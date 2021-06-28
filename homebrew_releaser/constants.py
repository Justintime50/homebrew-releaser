import os

# User Input
FORMULA_FOLDER = os.getenv('INPUT_FORMULA_FOLDER', 'formula')
GITHUB_TOKEN = os.getenv('INPUT_GITHUB_TOKEN')

# App Constants
SUBPROCESS_TIMEOUT = 30
GITHUB_HEADERS = {
    'accept': 'application/vnd.github.v3+json',
    'agent': 'Homebrew Releaser'
}
TAR_ARCHIVE = 'tar_archive.tar.gz'
