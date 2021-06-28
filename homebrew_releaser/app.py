import logging
import os

from homebrew_releaser.checksum import Checksum
from homebrew_releaser.constants import (FORMULA_FOLDER, GITHUB_TOKEN,
                                         TAR_ARCHIVE)
from homebrew_releaser.formula import Formula
from homebrew_releaser.git import Git
from homebrew_releaser.readme_updater import ReadmeUpdater
from homebrew_releaser.utils import Utils

GITHUB_BASE_URL = 'https://api.github.com'

# GitHub Action env variables set by GitHub
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY', 'user/repo').split('/')
GITHUB_OWNER = GITHUB_REPOSITORY[0]
GITHUB_REPO = GITHUB_REPOSITORY[1]

# Required GitHub Action env variables from user
INSTALL = os.getenv('INPUT_INSTALL')
HOMEBREW_OWNER = os.getenv('INPUT_HOMEBREW_OWNER')
HOMEBREW_TAP = os.getenv('INPUT_HOMEBREW_TAP')

# Optional GitHub Action env variables from user
COMMIT_OWNER = os.getenv('INPUT_COMMIT_OWNER', 'homebrew-releaser')
COMMIT_EMAIL = os.getenv('INPUT_COMMIT_EMAIL', 'homebrew-releaser@example.com')
TEST = os.getenv('INPUT_TEST')
SKIP_COMMIT = os.getenv('INPUT_SKIP_COMMIT', False)
UPDATE_README_TABLE = os.getenv('INPUT_UPDATE_README_TABLE')
DEBUG = os.getenv('INPUT_DEBUG', False)


class App():
    @staticmethod
    def run_github_action():
        """Runs the complete GitHub Action workflow

        1. Setup logging
        2. Grab the details about the tap
        3. Download the latest tar archive
        4. Generate a checksum
        5. Generate the new formula
        6. Update README table (optional)
        7. Add, commit, and push to GitHub
        """
        if DEBUG:
            logging_level = logging.DEBUG
        else:
            logging_level = logging.INFO

        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info('Starting Homebrew Releaser...')
        App.check_required_env_variables()

        logging.info('Setting up git environment...')
        Git.setup(COMMIT_OWNER, COMMIT_EMAIL, HOMEBREW_OWNER, HOMEBREW_TAP)

        logging.info(f'Collecting data about {GITHUB_REPO}...')
        repository = Utils.make_get_request(
            f'{GITHUB_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}',
            False
        ).json()
        tags = Utils.make_get_request(
            f'{GITHUB_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/tags',
            False
        ).json()
        version = tags[0]['name']
        logging.info(f'Latest release of {version} successfully identified...')
        tar_url = f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/archive/{version}.tar.gz'

        logging.info('Generating tar archive checksum...')
        App.download_latest_tar_archive(tar_url)
        checksum = Checksum.get_checksum(TAR_ARCHIVE)

        logging.info(f'Generating Homebrew formula for {GITHUB_REPO}...')
        template = Formula.generate_formula_data(
            GITHUB_OWNER,
            GITHUB_REPO,
            repository,
            checksum,
            INSTALL,
            tar_url,
            TEST,
        )

        Utils.write_file(f'{HOMEBREW_TAP}/{FORMULA_FOLDER}/{repository["name"]}.rb', template, 'w')

        if UPDATE_README_TABLE:
            logging.info('Attempting to update the README\'s project table...')
            ReadmeUpdater.update_readme(HOMEBREW_TAP)
        else:
            logging.debug('Skipping update to project README.')

        if SKIP_COMMIT:
            logging.info(f'Skipping commit to {HOMEBREW_TAP}.')
        else:
            logging.info(f'Attempting to release {version} of {GITHUB_REPO} to {HOMEBREW_TAP}...')
            Git.add(HOMEBREW_TAP)
            Git.commit(HOMEBREW_TAP, GITHUB_REPO, version)
            Git.push(HOMEBREW_TAP, HOMEBREW_OWNER)
            # TODO: Check the remote repo to ensure it got the new commit
            logging.info(f'Successfully released {version} of {GITHUB_REPO} to {HOMEBREW_TAP}!')

    @staticmethod
    def check_required_env_variables():
        """Checks that all required env variables are set
        """
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
        logging.debug('All required environment variables are present.')

    @staticmethod
    def download_latest_tar_archive(url):
        """Download the latest tar archive from GitHub
        """
        response = Utils.make_get_request(url, True)
        Utils.write_file(TAR_ARCHIVE, response.content, 'wb')


def main():
    App.run_github_action()


if __name__ == '__main__':
    main()
