import os

import woodchips

from homebrew_releaser.checksum import Checksum
from homebrew_releaser.constants import (
    CHECKSUM_FILE,
    FORMULA_FOLDER,
    GITHUB_OWNER,
    GITHUB_REPO,
    GITHUB_TOKEN,
    HOMEBREW_TAP,
    LOGGER_NAME,
    SKIP_COMMIT,
    TARGET_DARWIN_AMD64,
    TARGET_DARWIN_ARM64,
    TARGET_LINUX_AMD64,
    TARGET_LINUX_ARM64,
)
from homebrew_releaser.formula import Formula
from homebrew_releaser.git import Git
from homebrew_releaser.readme_updater import ReadmeUpdater
from homebrew_releaser.utils import Utils


GITHUB_BASE_URL = 'https://api.github.com'

# Required GitHub Action env variables from user
INSTALL = os.getenv('INPUT_INSTALL')
HOMEBREW_OWNER = os.getenv('INPUT_HOMEBREW_OWNER')

# Optional GitHub Action env variables from user
COMMIT_OWNER = os.getenv('INPUT_COMMIT_OWNER', 'homebrew-releaser')
COMMIT_EMAIL = os.getenv('INPUT_COMMIT_EMAIL', 'homebrew-releaser@example.com')
DEPENDS_ON = os.getenv('INPUT_DEPENDS_ON')
TEST = os.getenv('INPUT_TEST')
UPDATE_README_TABLE = (
    os.getenv('INPUT_UPDATE_README_TABLE', False) if os.getenv('INPUT_UPDATE_README_TABLE') != 'false' else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string
DEBUG = (
    os.getenv('INPUT_DEBUG', False) if os.getenv('INPUT_DEBUG') != 'false' else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string


class App:
    @staticmethod
    def run_github_action():
        """Runs the complete GitHub Action workflow.

        1. Setup logging
        2. Grab the details about the tap
        3. Download the tar archive(s)
        4. Generate checksum(s)
        5. Generate the new formula
        6. Update README table (optional)
        7. Add, commit, and push updated formula to GitHub
        """
        App.setup_logger()
        logger = woodchips.get(LOGGER_NAME)

        logger.info('Starting Homebrew Releaser...')
        App.check_required_env_variables()

        logger.info('Setting up git environment...')
        Git.setup(COMMIT_OWNER, COMMIT_EMAIL, HOMEBREW_OWNER, HOMEBREW_TAP)

        logger.info(f'Collecting data about {GITHUB_REPO}...')
        repository = Utils.make_github_get_request(url=f'{GITHUB_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}').json()
        latest_release = Utils.make_github_get_request(
            url=f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest'
        ).json()
        assets = latest_release['assets']
        version = latest_release['tag_name']
        version_no_v = version.replace('v', '')
        logger.info(f'Latest release ({version}) successfully identified!')

        logger.info('Generating tar archive checksum(s)...')
        archive_urls = []

        # Auto-generated tar URL must come first for later use
        auto_generated_release_tar = f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/archive/{version}.tar.gz'
        archive_urls.append(auto_generated_release_tar)

        auto_generated_release_zip = f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/archive/{version}.zip'
        archive_urls.append(auto_generated_release_zip)

        # We check if matching browser URLs exist but use the asset URL so that this works for
        # both public and private repos since the browser URL isn't accessible via private repos
        if TARGET_DARWIN_AMD64:
            darwin_amd64_browser_url = f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download/{version}/{GITHUB_REPO}-{version_no_v}-darwin-amd64.tar.gz'  # noqa
            for asset in assets:
                if asset['browser_download_url'] == darwin_amd64_browser_url:
                    archive_urls.append(asset['url'])
                    break
        if TARGET_DARWIN_ARM64:
            darwin_arm64_browser_url = f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download/{version}/{GITHUB_REPO}-{version_no_v}-darwin-arm64.tar.gz'  # noqa
            for asset in assets:
                if asset['browser_download_url'] == darwin_arm64_browser_url:
                    archive_urls.append(asset['url'])
                    break
        if TARGET_LINUX_AMD64:
            linux_amd64_browser_url = f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download/{version}/{GITHUB_REPO}-{version_no_v}-linux-amd64.tar.gz'  # noqa
            for asset in assets:
                if asset['browser_download_url'] == linux_amd64_browser_url:
                    archive_urls.append(asset['url'])
                    break
        if TARGET_LINUX_ARM64:
            linux_arm64_browser_url = f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download/{version}/{GITHUB_REPO}-{version_no_v}-linux-arm64.tar.gz'  # noqa
            for asset in assets:
                if asset['browser_download_url'] == linux_arm64_browser_url:
                    archive_urls.append(asset['url'])
                    break

        checksums = []
        for archive_url in archive_urls:
            archive_filename = App.download_archive(archive_url)
            checksum = Checksum.get_checksum(archive_filename)
            archive_checksum_entry = f'{checksum} {archive_filename}'
            checksums.append(
                {
                    archive_filename: {
                        'checksum': checksum,
                        'url': archive_url,
                    }
                },
            )

            Utils.write_file(CHECKSUM_FILE, archive_checksum_entry, 'a')

        logger.info(f'Generating Homebrew formula for {GITHUB_REPO}...')
        template = Formula.generate_formula_data(
            GITHUB_OWNER,
            GITHUB_REPO,
            repository,
            checksums,
            INSTALL,
            auto_generated_release_tar,
            DEPENDS_ON,
            TEST,
        )

        Utils.write_file(os.path.join(HOMEBREW_TAP, FORMULA_FOLDER, f'{repository["name"]}.rb'), template, 'w')

        if UPDATE_README_TABLE:
            logger.info('Attempting to update the README\'s project table...')
            ReadmeUpdater.update_readme(HOMEBREW_TAP)
        else:
            logger.debug('Skipping update to project README.')

        if SKIP_COMMIT:
            logger.info(f'Skipping upload of checksum.txt to {HOMEBREW_TAP}.')
            logger.info(f'Skipping commit to {HOMEBREW_TAP}.')
        else:
            logger.info(f'Attempting to upload checksum.txt to the latest release of {GITHUB_REPO}...')
            Checksum.upload_checksum_file(latest_release)

            logger.info(f'Attempting to release {version} of {GITHUB_REPO} to {HOMEBREW_TAP}...')
            Git.add(HOMEBREW_TAP)
            Git.commit(HOMEBREW_TAP, GITHUB_REPO, version)
            Git.push(HOMEBREW_TAP, HOMEBREW_OWNER)
            logger.info(f'Successfully released {version} of {GITHUB_REPO} to {HOMEBREW_TAP}!')

    @staticmethod
    def setup_logger():
        """Setup a `woodchips` logger instance."""
        logging_level = 'DEBUG' if DEBUG else 'INFO'

        logger = woodchips.Logger(
            name=LOGGER_NAME,
            level=logging_level,
        )
        logger.log_to_console(formatter='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def check_required_env_variables():
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
                    'You must provide all necessary environment variables. Please reference the Homebrew Releaser documentation.'  # noqa
                )
        logger.debug('All required environment variables are present.')

    @staticmethod
    def download_archive(url: str) -> str:
        """Gets an archive (eg: zip, tar) from GitHub and saves it locally."""
        response = Utils.make_github_get_request(
            url=url,
            stream=True,
        )
        filename = url.rsplit('/', 1)[1]
        Utils.write_file(filename, response.content, 'wb')

        return filename


def main():
    App.run_github_action()


if __name__ == '__main__':
    main()
