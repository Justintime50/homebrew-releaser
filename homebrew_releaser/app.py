import os
from typing import Optional

import woodchips

from homebrew_releaser._version import __version__
from homebrew_releaser.checksum import (
    calculate_checksum,
    upload_checksum_file,
)
from homebrew_releaser.constants import (
    BRANCH,
    CHECKSUM_FILE,
    COMMIT_EMAIL,
    COMMIT_OWNER,
    CUSTOM_REQUIRE,
    CUSTOM_TARBALL,
    DEBUG,
    DEPENDS_ON,
    DOWNLOAD_STRATEGY,
    FORMULA_INCLUDES,
    GITHUB_BASE_API_URL,
    GITHUB_BASE_URL,
    GITHUB_OWNER,
    GITHUB_REPO,
    GITHUB_TOKEN,
    HOMEBREW_OWNER,
    HOMEBREW_TAP,
    IGNORE_WARNINGS,
    INSTALL,
    LOGGER_NAME,
    SKIP_CHECKSUM,
    SKIP_COMMIT,
    TARGET_DARWIN_AMD64,
    TARGET_DARWIN_ARM64,
    TARGET_LINUX_AMD64,
    TARGET_LINUX_ARM64,
    TEST,
    UPDATE_PYTHON_RESOURCES,
    UPDATE_README_TABLE,
    VERSION,
    non_critical_warnings,
)
from homebrew_releaser.formula import generate_formula_data
from homebrew_releaser.git import (
    add_git,
    commit_git,
    copy_formula_file_to_git,
    make_formula_folder,
    push_git,
    setup_git,
)
from homebrew_releaser.homebrew import (
    get_homebrew_version,
    setup_homebrew_tap,
    update_python_resources,
)
from homebrew_releaser.readme_updater import update_readme
from homebrew_releaser.utils import (
    get_filename_from_path,
    make_github_get_request,
    write_file,
)


def run_github_action():
    """Runs the complete GitHub Action workflow.

    1. Setup logging
    2. Setup git environment
    3. Setup Homebrew tap
    4. Grab the details about the tap
    5. Download the archive(s)
    6. Generate checksum(s)
    7. Generate the new formula
    8. Update README table (optional)
    9. Add, commit, and push updated formula to GitHub
    10. Upload checksum.txt to latest release (optional)
    11. Raise non-critical warnings at the end so release succeeds but users are aware
    """
    _setup_logger()
    logger = woodchips.get(LOGGER_NAME)

    logger.info(f"Starting Homebrew Releaser v{__version__}...")
    homebrew_version = get_homebrew_version()
    logger.info(f"Using {homebrew_version}.")
    _check_required_env_variables()

    logger.info("Setting up git environment...")
    setup_git(COMMIT_OWNER, COMMIT_EMAIL, HOMEBREW_OWNER, HOMEBREW_TAP)

    logger.info("Setting up Homebrew tap...")
    setup_homebrew_tap(HOMEBREW_OWNER, HOMEBREW_TAP)
    make_formula_folder(HOMEBREW_TAP)

    logger.info(f"Collecting data about {GITHUB_REPO}...")
    repository = make_github_get_request(url=f"{GITHUB_BASE_API_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}").json()
    latest_release = make_github_get_request(
        url=f"{GITHUB_BASE_API_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    ).json()
    assets = latest_release["assets"]
    version = VERSION or latest_release["tag_name"]
    version_no_v = version.lstrip("v")
    logger.info(f"Latest release ({version}) successfully identified.")

    logger.info("Generating tar archive checksum(s)...")
    archive_urls = []
    archive_checksum_entries = ""

    # Auto-generated tar URL must come first for later use (order is important)
    if repository["private"]:
        logger.debug("Repository is private. Using auto-generated release tarball and zipball REST API endpoints.")
        archive_base_url = f"{GITHUB_BASE_API_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
        auto_generated_release_tar_url = f"{archive_base_url}/tarball/{version}"
        auto_generated_release_zip_url = f"{archive_base_url}/zipball/{version}"
    else:
        logger.debug("Repository is public. Using auto-generated release tarball and zipball public URLs.")
        archive_base_url = f"{GITHUB_BASE_URL}/{GITHUB_OWNER}/{GITHUB_REPO}/archive/refs/tags/{version}"
        auto_generated_release_tar_url = f"{archive_base_url}.tar.gz"
        auto_generated_release_zip_url = f"{archive_base_url}.zip"

    archive_urls.append(auto_generated_release_tar_url)
    archive_urls.append(auto_generated_release_zip_url)

    target_browser_download_base_url = (
        f"{GITHUB_BASE_URL}/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download/{version}/{GITHUB_REPO}-{version_no_v}"
    )
    if TARGET_DARWIN_AMD64:
        archive_urls.append(f"{target_browser_download_base_url}-darwin-amd64.tar.gz")
    if TARGET_DARWIN_ARM64:
        archive_urls.append(f"{target_browser_download_base_url}-darwin-arm64.tar.gz")
    if TARGET_LINUX_AMD64:
        archive_urls.append(f"{target_browser_download_base_url}-linux-amd64.tar.gz")
    if TARGET_LINUX_ARM64:
        archive_urls.append(f"{target_browser_download_base_url}-linux-arm64.tar.gz")

    custom_tarball_url = None
    if CUSTOM_TARBALL:
        custom_tarball_url = (
            f"{GITHUB_BASE_URL}/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download/{version}/{CUSTOM_TARBALL}.tar.gz"
        )
        logger.debug(
            f"Using the following custom tarball URL instead of auto-generated tarball URL: {custom_tarball_url}"
        )
        archive_urls.append(custom_tarball_url)

    checksums = []
    for archive_url in archive_urls:
        if repository["private"]:
            # For private repos, use asset["url"] if available, otherwise use archive_url
            matching_asset = next(
                (asset for asset in assets if asset and asset.get("browser_download_url") == archive_url), None
            )
            download_url = matching_asset["url"] if matching_asset else archive_url
            stream = False
        else:
            # For public repos, always use browser URLs
            download_url = archive_url
            stream = True

        downloaded_filename = _download_archive(download_url, stream)
        checksum = calculate_checksum(downloaded_filename)
        archive_filename = get_filename_from_path(archive_url)
        archive_checksum_entries += f"{checksum} {archive_filename}\n"
        checksums.append(
            {
                archive_filename: {
                    "checksum": checksum,
                    "url": archive_url,
                }
            }
        )

    write_file(CHECKSUM_FILE, archive_checksum_entries)

    logger.info(f"Generating Homebrew formula for {GITHUB_REPO}...")
    template = generate_formula_data(
        GITHUB_OWNER,
        GITHUB_REPO,
        repository,
        checksums,
        INSTALL,
        custom_tarball_url or auto_generated_release_tar_url,
        DEPENDS_ON,
        TEST,
        DOWNLOAD_STRATEGY,
        CUSTOM_REQUIRE,
        FORMULA_INCLUDES,
        UPDATE_PYTHON_RESOURCES,
        version_no_v if VERSION else None,
    )

    formula_filename = f"{repository['name']}.rb"
    formula_dir = os.path.join(
        os.sep,
        "home",
        "linuxbrew",
        ".linuxbrew",
        "Homebrew",
        "Library",
        "Taps",
        HOMEBREW_OWNER,
        HOMEBREW_TAP,
    )
    formula_filepath = os.path.join(formula_dir, formula_filename)
    write_file(formula_filepath, template, "w")

    if UPDATE_PYTHON_RESOURCES:
        logger.info("Attempting to update Python resources in the formula...")
        update_python_resources(formula_dir, formula_filename)
        if DEBUG:
            with open(formula_filepath, "r") as formula_file:
                formula_content = formula_file.read()
                logger.debug(formula_content)
    else:
        logger.debug("Skipping update to Python resources.")

    if UPDATE_README_TABLE:
        logger.info("Attempting to update the README's project table...")
        update_readme(HOMEBREW_TAP)
    else:
        logger.debug("Skipping update to project README.")

    # Although users can skip a commit, still commit (but don't push) to dry-run the commit for debugging purposes
    logger.info("Preparing git commit...")
    copy_formula_file_to_git(formula_filepath, HOMEBREW_TAP)
    add_git(HOMEBREW_TAP)
    commit_git(HOMEBREW_TAP, GITHUB_REPO, version)

    if SKIP_COMMIT:
        logger.info(f"Skipping push to {HOMEBREW_TAP}.")
        logger.info(f"Skipping upload of checksum.txt to {HOMEBREW_TAP}.")
    else:
        logger.info(f"Attempting to release {version} of {GITHUB_REPO} to {HOMEBREW_TAP}...")
        push_git(HOMEBREW_TAP, HOMEBREW_OWNER, BRANCH)
        if SKIP_CHECKSUM:
            logger.info(f"Skipping upload of checksum.txt to {HOMEBREW_TAP}.")
        else:
            logger.info(f"Attempting to upload checksum.txt to the latest release of {GITHUB_REPO}...")
            upload_checksum_file(latest_release)
        logger.info(f"Successfully released {version} of {GITHUB_REPO} to {HOMEBREW_TAP}.")

    if non_critical_warnings and not IGNORE_WARNINGS:
        logger.info("The following non-critical warnings were raised during execution:")
        for i, warning in enumerate(non_critical_warnings):
            logger.warning(f"{i + 1}. {warning}")
        raise SystemExit(
            "Your release most likely succeeded (check logs above); however, we are failing the build to surface these non-critical warnings to you."  # noqa
        )


def _setup_logger():
    """Setup a `woodchips` logger instance."""
    logging_level = "DEBUG" if DEBUG else "INFO"

    logger = woodchips.Logger(
        name=LOGGER_NAME,
        level=logging_level,
    )
    logger.log_to_console(formatter="%(asctime)s - %(levelname)s - %(message)s")


def _check_required_env_variables():
    """Checks that all required env variables are set."""
    logger = woodchips.get(LOGGER_NAME)

    required_env_variables = [
        GITHUB_TOKEN,
        HOMEBREW_OWNER,
        HOMEBREW_TAP,
        INSTALL,
    ]

    for env_variable in required_env_variables:
        if not env_variable:
            raise SystemExit(
                "You must provide all necessary environment variables. Please reference the Homebrew Releaser documentation."  # noqa
            )
    logger.debug("All required environment variables are present.")


def _download_archive(url: str, stream: Optional[bool] = False) -> str:
    """Gets an archive (eg: zip, tar) from GitHub and saves it locally."""
    response = make_github_get_request(
        url=url,
        stream=stream,
    )
    filename = get_filename_from_path(url)
    write_file(filename, response.content, "wb")

    return filename


def main():
    run_github_action()


if __name__ == "__main__":
    main()
