import os

import woodchips

from homebrew_releaser.checksum import Checksum
from homebrew_releaser.constants import (
    FORMULA_FOLDER,
    GITHUB_OWNER,
    GITHUB_REPO,
    GITHUB_TOKEN,
    HOMEBREW_TAP,
    LOGGER_NAME,
    SKIP_COMMIT,
    TAR_ARCHIVE,
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
UPDATE_README_TABLE = os.getenv('INPUT_UPDATE_README_TABLE', False)
DEBUG = os.getenv('INPUT_DEBUG', False)


class App:
    @staticmethod
    def run_github_action():
        """Runs the complete GitHub Action workflow.

        1. Setup logging
        2. Grab the details about the tap
        3. Download the tar archive(s)
        4. Generate a checksum
        5. Generate the new formula
        6. Update README table (optional)
        7. Add, commit, and push to GitHub
        """
        App.setup_logger()
        logger = woodchips.get(LOGGER_NAME)

        logger.info('Starting Homebrew Releaser...')
        App.check_required_env_variables()

        logger.info('Setting up git environment...')
        Git.setup(COMMIT_OWNER, COMMIT_EMAIL, HOMEBREW_OWNER, HOMEBREW_TAP)

        logger.info(f'Collecting data about {GITHUB_REPO}...')
        repository = Utils.make_get_request(f'{GITHUB_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}', False).json()
        tags = Utils.make_get_request(f'{GITHUB_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/tags', False).json()
        version = tags[0]['name']
        logger.info(f'Latest release ({version}) successfully identified...')

        logger.info('Generating tar archive checksum(s)...')
        auto_generated_release_tar = f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/archive/{version}.tar.gz'
        # When introducing multiple tar URLs, iterate them here and download/checksum each below. Conditionally
        # use the default auto_generated release ^. Ref: https://github.com/Justintime50/homebrew-releaser/issues/9
        App.download_tar_archive(auto_generated_release_tar)
        checksum, checksum_file = Checksum.get_checksum(TAR_ARCHIVE)
        archive_checksum_entry = f'{checksum} {checksum_file}'
        Utils.write_file('checksum.txt', archive_checksum_entry, 'a')

        logger.info(f'Generating Homebrew formula for {GITHUB_REPO}...')
        template = Formula.generate_formula_data(
            GITHUB_OWNER,
            GITHUB_REPO,
            repository,
            checksum,
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
            Checksum.upload_checksum_file()

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
    def download_tar_archive(url: str):
        """Gets a tar archive from GitHub and saves it locally."""
        response = Utils.make_get_request(url, True)
        Utils.write_file(TAR_ARCHIVE, response.content, 'wb')


def main():
    App.run_github_action()


if __name__ == '__main__':
    main()
