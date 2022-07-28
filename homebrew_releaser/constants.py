import os

# User Input
FORMULA_FOLDER = os.getenv('INPUT_FORMULA_FOLDER', 'formula')
GITHUB_TOKEN = os.getenv('INPUT_GITHUB_TOKEN')
HOMEBREW_TAP = os.getenv('INPUT_HOMEBREW_TAP')
SKIP_COMMIT = os.getenv('INPUT_SKIP_COMMIT', False)

# App Constants
LOGGER_NAME = 'homebrew-releaser'
SUBPROCESS_TIMEOUT = 30
GITHUB_HEADERS = {
    'accept': 'application/vnd.github.v3+json',
    'agent': 'Homebrew Releaser',
}
TAR_ARCHIVE = 'tar_archive.tar.gz'
CHECKSUM_FILE = 'checksum.txt'

# GitHub Action env variables set by GitHub
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY', 'user/repo').split('/')
GITHUB_OWNER = GITHUB_REPOSITORY[0]
GITHUB_REPO = GITHUB_REPOSITORY[1]
