import os

# For constants that are required by multiple modules

# TODO: Clean this up
SUBPROCESS_TIMEOUT = 30
FORMULA_FOLDER = os.getenv('INPUT_FORMULA_FOLDER', 'formula')
GITHUB_HEADERS = {
    'accept': 'application/vnd.github.v3+json',
    'agent': 'Homebrew Releaser'
}
GITHUB_TOKEN = os.getenv('INPUT_GITHUB_TOKEN')
TAR_ARCHIVE = 'tar_archive.tar.gz'
