import logging
import os

# from homebrew_releaser.checksum import get_checksum
# from homebrew_releaser.commit import commit_formula
from homebrew_releaser.constants import (FORMULA_FOLDER, GITHUB_TOKEN,
                                         TAR_ARCHIVE)
# from homebrew_releaser.readme_updater import update_readme
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


class App():
    # def run_github_action(self):
    #     """Runs the complete GitHub Action workflow
    #     """
    #     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    #     logging.info('Starting Homebrew Releaser...')
    #     self.check_required_env_variables()

    #     logging.info(f'Collecting data about {GITHUB_REPO}...')
    #     repository = make_get_request(f'{GITHUB_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}', False).json()
    #     tags = make_get_request(
    #         f'{GITHUB_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/tags', False
    #     ).json()
    #     version = tags[0]['name']
    #     tar_url = f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/archive/{version}.tar.gz'

    #     logging.info('Generating tar archive checksum...')
    #     self.get_latest_tar_archive(tar_url)
    #     checksum = get_checksum(TAR_ARCHIVE)

    #     logging.info(f'Generating Homebrew formula for {GITHUB_REPO}...')
    #     template = self.generate_formula(
    #         GITHUB_OWNER,
    #         GITHUB_REPO,
    #         repository,
    #         checksum,
    #         INSTALL,
    #         tar_url,
    #         TEST,
    #     )
    #     write_file(f'{HOMEBREW_TAP}/{FORMULA_FOLDER}/{repository["name"]}.rb', template, 'w')

    #     # TODO: We split up adding/committing/pushing so we need to add more steps with the right params
    #     if SKIP_COMMIT:  # TODO: Ensure this only skips the commit step but runs the rest
    #         logging.info(f'Skipping commit to {HOMEBREW_TAP}.')
    #     else:
    #         logging.info('Setting up git environment...')
    #         Git.setup(COMMIT_OWNER, COMMIT_EMAIL, HOMEBREW_OWNER, HOMEBREW_TAP)
    #         if UPDATE_README_TABLE:
    #             logging.info('Attempting to update the README\'s project table...')
    #             update_readme(HOMEBREW_TAP)
    #         logging.info(f'Attempting to release {version} of {GITHUB_REPO} to {HOMEBREW_TAP}...')
    #         commit_formula(HOMEBREW_OWNER, HOMEBREW_TAP, FORMULA_FOLDER, GITHUB_REPO, version)
    #         logging.info(f'Successfully released {version} of {GITHUB_REPO} to {HOMEBREW_TAP}!')

    # def check_required_env_variables(self):
    #     """Checks that all required env variables are set
    #     """
    #     required_env_variables = [
    #         GITHUB_TOKEN,
    #         INSTALL,
    #         HOMEBREW_OWNER,
    #         HOMEBREW_TAP
    #     ]
    #     for env_variable in required_env_variables:
    #         if not env_variable:
    #             raise SystemExit((
    #                 'You must provide all necessary environment variables. Please reference the Homebrew Releaser documentation.'  # noqa
    #             ))
    #     logging.debug('All required environment variables are present.')

    @staticmethod
    def get_latest_tar_archive(url):
        """Download the latest tar archive from GitHub
        """
        response = Utils.make_get_request(url, True)
        Utils.write_file(TAR_ARCHIVE, response.content, 'wb')


def main():
    App.run_github_action()


if __name__ == '__main__':
    main()
