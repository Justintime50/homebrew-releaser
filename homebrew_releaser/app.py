import os
from typing import Optional

import woodchips

from homebrew_releaser._version import __version__
from homebrew_releaser.checksum import (
    calculate_checksum,
    upload_checksum_file,
)
from homebrew_releaser.constants import (
    CHECKSUM_FILE,
    CUSTOM_REQUIRE,
    DOWNLOAD_STRATEGY,
    FORMULA_INCLUDES,
    GITHUB_OWNER,
    GITHUB_REPO,
    GITHUB_TOKEN,
    HOMEBREW_TAP,
    LOGGER_NAME,
    SKIP_CHECKSUM,
    SKIP_COMMIT,
    TARGET_DARWIN_AMD64,
    TARGET_DARWIN_ARM64,
    TARGET_LINUX_AMD64,
    TARGET_LINUX_ARM64,
    UPDATE_PYTHON_RESOURCES,
    VERSION,
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


GITHUB_BASE_URL = "https://api.github.com"

# Required GitHub Action env variables from user
INSTALL = os.getenv("INPUT_INSTALL")
HOMEBREW_OWNER = os.getenv("INPUT_HOMEBREW_OWNER", "").lower()

# Optional GitHub Action env variables from user
COMMIT_OWNER = os.getenv("INPUT_COMMIT_OWNER", "homebrew-releaser")
COMMIT_EMAIL = os.getenv("INPUT_COMMIT_EMAIL", "homebrew-releaser@example.com")
DEPENDS_ON = os.getenv("INPUT_DEPENDS_ON")
TEST = os.getenv("INPUT_TEST")
UPDATE_README_TABLE = (
    os.getenv("INPUT_UPDATE_README_TABLE", False) if os.getenv("INPUT_UPDATE_README_TABLE") != "false" else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string
DEBUG = (
    os.getenv("INPUT_DEBUG", False) if os.getenv("INPUT_DEBUG") != "false" else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string


def run_github_action():
    """Runs the complete GitHub Action workflow.

    1. Setup logging
    2. Grab the details about the tap
    3. Download the archive(s)
    4. Generate checksum(s)
    5. Generate the new formula
    6. Update README table (optional)
    7. Add, commit, and push updated formula to GitHub
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
    repository = make_github_get_request(url=f"{GITHUB_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}").json()
    latest_release = make_github_get_request(
        url=f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
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
        archive_base_url = f"{GITHUB_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}"
        auto_generated_release_tar = f"{archive_base_url}/tarball/{version}"
        auto_generated_release_zip = f"{archive_base_url}/zipball/{version}"
    else:
        logger.debug("Repository is public. Using auto-generated release tarball and zipball public URLs.")
        archive_base_url = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/archive/refs/tags/{version}"
        auto_generated_release_tar = f"{archive_base_url}.tar.gz"
        auto_generated_release_zip = f"{archive_base_url}.zip"

    archive_urls.append(auto_generated_release_tar)
    archive_urls.append(auto_generated_release_zip)

    target_browser_download_base_url = (
        f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download/{version}/{GITHUB_REPO}-{version_no_v}"
    )
    if TARGET_DARWIN_AMD64:
        archive_urls.append(f"{target_browser_download_base_url}-darwin-amd64.tar.gz")
    if TARGET_DARWIN_ARM64:
        archive_urls.append(f"{target_browser_download_base_url}-darwin-arm64.tar.gz")
    if TARGET_LINUX_AMD64:
        archive_urls.append(f"{target_browser_download_base_url}-linux-amd64.tar.gz")
    if TARGET_LINUX_ARM64:
        archive_urls.append(f"{target_browser_download_base_url}-linux-arm64.tar.gz")

    checksums = []
    for archive_url in archive_urls:
        if not assets:
            assets = [0]  # Populate `assets` so that if we don't have any, we can use the auto generated checksums
        for asset in assets:
            # Download the asset url so private repos work but use the brower URL for name and path in formula
            if archive_url == auto_generated_release_tar or archive_url == auto_generated_release_zip:
                download_url = archive_url
            else:
                download_url = asset["url"]

            if (
                archive_url == auto_generated_release_tar
                or archive_url == auto_generated_release_zip
                or archive_url == asset["browser_download_url"]
            ):
                # For REST API requests, we should not stream archive file, but it is fine for browser URLs
                stream = False if archive_url.find("api.github.com") != -1 else True
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
                    },
                )
                # We break here so we don't include duplicate checksums for the auto generated URLs
                break

    write_file(CHECKSUM_FILE, archive_checksum_entries)

    logger.info(f"Generating Homebrew formula for {GITHUB_REPO}...")
    template = generate_formula_data(
        GITHUB_OWNER,
        GITHUB_REPO,
        repository,
        checksums,
        INSTALL,
        auto_generated_release_tar,
        DEPENDS_ON,
        TEST,
        DOWNLOAD_STRATEGY,
        CUSTOM_REQUIRE,
        FORMULA_INCLUDES,
        UPDATE_PYTHON_RESOURCES,
        version_no_v if VERSION else None,
    )

    formula_filename = f'{repository["name"]}.rb'
    formula_dir = os.path.join(
        os.path.expanduser("~"),  # Linuxbrew home directory
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
    copy_formula_file_to_git(formula_filepath, HOMEBREW_TAP)
    add_git(HOMEBREW_TAP)
    commit_git(HOMEBREW_TAP, GITHUB_REPO, version)

    if SKIP_COMMIT:
        logger.info(f"Skipping push to {HOMEBREW_TAP}.")
        logger.info(f"Skipping upload of checksum.txt to {HOMEBREW_TAP}.")
    else:
        logger.info(f"Attempting to release {version} of {GITHUB_REPO} to {HOMEBREW_TAP}...")
        push_git(HOMEBREW_TAP, HOMEBREW_OWNER)
        if SKIP_CHECKSUM:
            logger.info(f"Skipping upload of checksum.txt to {HOMEBREW_TAP}.")
        else:
            logger.info(f"Attempting to upload checksum.txt to the latest release of {GITHUB_REPO}...")
            upload_checksum_file(latest_release)
        logger.info(f"Successfully released {version} of {GITHUB_REPO} to {HOMEBREW_TAP}.")


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
