import logging
import os
import re
import subprocess

import requests

GITHUB_BASE_URL = 'https://api.github.com'
GITHUB_HEADERS = {
    'accept': 'application/vnd.github.v3+json',
    'agent': 'Homebrew Releaser'
}
SUBPROCESS_TIMEOUT = 30
TAR_ARCHIVE = 'tar_archive.tar.gz'

# GitHub Action env variables set by GitHub
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY').split('/')
GITHUB_OWNER = GITHUB_REPOSITORY[0]
GITHUB_REPO = GITHUB_REPOSITORY[1]

# Required GitHub Action env variables from user
GITHUB_TOKEN = os.getenv('INPUT_GITHUB_TOKEN')
INSTALL = os.getenv('INPUT_INSTALL')
HOMEBREW_OWNER = os.getenv('INPUT_HOMEBREW_OWNER')
HOMEBREW_TAP = os.getenv('INPUT_HOMEBREW_TAP')

# Optional GitHub Action env variables from user
COMMIT_OWNER = os.getenv('INPUT_COMMIT_OWNER', 'homebrew-releaser')
COMMIT_EMAIL = os.getenv('INPUT_COMMIT_EMAIL', 'homebrew-releaser@example.com')
FORMULA_FOLDER = os.getenv('INPUT_FORMULA_FOLDER', 'formula')
TEST = os.getenv('INPUT_TEST')


def run_github_action():
    """Runs the complete GitHub Action workflow
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting Homebrew Releaser...')
    check_required_env_variables()

    logging.info(f'Collecting data about {GITHUB_REPO}...')
    repository = make_get_request(f'{GITHUB_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}', False).json()
    latest_release = make_get_request(
        f'{GITHUB_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest', False
    ).json()
    version = latest_release['name']
    tar_url = f'https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/archive/{version}.tar.gz'

    logging.info('Generating tar archive checksum...')
    get_latest_tar_archive(tar_url)
    checksum = get_checksum(TAR_ARCHIVE)

    logging.info(f'Generating Homebrew formula for {GITHUB_REPO}...')
    template = generate_formula(
        GITHUB_OWNER,
        GITHUB_REPO,
        version,
        repository,
        checksum,
        INSTALL,
        tar_url,
        TEST,
    )
    write_file(f'new_{repository["name"]}.rb', template, 'w')

    logging.info(f'Attempting to release {version} of {GITHUB_REPO} to {HOMEBREW_TAP}...')
    commit_formula(COMMIT_OWNER, COMMIT_EMAIL, HOMEBREW_OWNER,
                   HOMEBREW_TAP, FORMULA_FOLDER, GITHUB_REPO, version)
    logging.info(f'Successfully released {version} of {GITHUB_REPO} to {HOMEBREW_TAP}!')


def check_required_env_variables():
    """Checks that all required env variables are set
    """
    required_env_variables = [
        GITHUB_TOKEN,
        INSTALL,
        HOMEBREW_OWNER,
        HOMEBREW_TAP
    ]
    for env_variable in required_env_variables:
        if not env_variable:
            raise SystemExit((
                'You must provide all necessary environment variables.\n'
                'Please reference the Homebrew Releaser documentation.'
            ))
    logging.debug('All required environment variables are present.')


def make_get_request(url, stream=False):
    """Make an HTTP GET request
    """
    try:
        response = requests.get(
            url,
            headers=GITHUB_HEADERS,
            stream=stream
        )
        logging.debug(f'HTTP GET request made successfully to {url}.')
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)
    return response


def get_latest_tar_archive(url):
    """Download the latest tar archive
    """
    response = make_get_request(url, True)
    write_file(TAR_ARCHIVE, response.content, 'wb')


def write_file(filename, content, mode='w'):
    """Writes content to a file
    """
    try:
        with open(filename, mode) as f:
            f.write(content)
        logging.debug(f'{filename} written successfully.')
    except Exception as error:
        raise SystemExit(error)


def get_checksum(tar_file):
    """Gets the checksum of a file
    """
    # TODO: Create and upload a `checksums.txt` file to the release for the zip and tar archives
    try:
        output = subprocess.check_output(
            f'shasum -a 256 {tar_file}',
            stdin=None,
            stderr=None,
            shell=True,
            timeout=SUBPROCESS_TIMEOUT
        )
        checksum = output.decode().split()[0]
        checksum_file = output.decode().split()[1]  # TODO: Use this to craft the `checksums.txt` file  # noqa
        logging.debug(f'{checksum} generated successfully.')
    except subprocess.TimeoutExpired as error:
        raise SystemExit(error)
    except subprocess.CalledProcessError as error:
        raise SystemExit(error)
    return checksum


def generate_formula(owner, repo_name, version, repository, checksum, install, tar_url, test):
    """Generates the formula file for Homebrew

    We attempt to ensure generated formula will pass `brew audit --strict --online` if given correct inputs:
    - Proper class name
    - 80 characters or less desc field (alphanumeric characters and does not start with an article)
    - Present homepage
    - URL points to the tar file
    - Checksum matches the url archive
    - Proper installable binary
    - Test is included
    """
    repo_name_length = len(repo_name) + 2  # We add 2 here to offset for spaces and a add buffer
    max_desc_field_length = 80
    description_length = max_desc_field_length - repo_name_length

    test = f"""
  test do
    {test.strip()}
  end
end
""" if test else 'end'

    template = f"""# typed: false
# frozen_string_literal: true

# This file was generated by Homebrew Releaser. DO NOT EDIT.
class {re.sub(r'[-_. ]+', '', repo_name.title())} < Formula
  desc "{re.sub(r'?![dw ]+', '', repository['description'][:description_length].strip())}"
  homepage "https://github.com/{owner}/{repo_name}"
  url "{tar_url}"
  sha256 "{checksum}"
  license "{repository['license']['spdx_id']}"
  bottle :unneeded

  def install
    {install.strip()}
  end
{test}
"""
    logging.debug('Homebrew formula generated successfully.')
    return template


def commit_formula(commit_owner, commit_email, homebrew_owner, homebrew_tap,
                   formula_folder, repo_name, version):
    """Commits the new formula to the specified Homebrew tap

    1) Set global git config for the commit
    2) Clone the Homebrew tap repo
    3) Move our generated formula into the homebrew tap repo
    4) Commit and push the updated formula file to the repo
    """
    try:
        output = subprocess.check_output(
            (
                f'git config --global user.name "{commit_owner}" && '
                f'git config --global user.email {commit_email} && '
                f'git clone --depth=5 https://{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git && '
                f'mv new_{repo_name}.rb {homebrew_tap}/{formula_folder}/{repo_name}.rb && '
                f'cd {homebrew_tap} && '
                f'git add {formula_folder}/{repo_name}.rb && '
                f'git commit -m "Brew formula update for {repo_name} version {version}" && '
                f'git push https://{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git'
            ),
            stdin=None,
            stderr=None,
            shell=True,
            timeout=SUBPROCESS_TIMEOUT
        )
        logging.debug(f'Formula committed successfully to {homebrew_tap}.')
    except subprocess.TimeoutExpired as error:
        raise SystemExit(error)
    except subprocess.CalledProcessError as error:
        raise SystemExit(error)
    return output


def main():
    run_github_action()


if __name__ == '__main__':
    main()
