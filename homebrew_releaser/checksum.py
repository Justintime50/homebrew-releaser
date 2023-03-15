import subprocess  # nosec
from typing import Any

import requests
import woodchips

from homebrew_releaser.constants import (
    CHECKSUM_FILE,
    GITHUB_HEADERS,
    GITHUB_OWNER,
    GITHUB_REPO,
    LOGGER_NAME,
    TIMEOUT,
)


class Checksum:
    @staticmethod
    def get_checksum(tar_filepath: str) -> str:
        """Gets the checksum of a file."""
        logger = woodchips.get(LOGGER_NAME)

        try:
            command = ['shasum', '-a', '256', tar_filepath]
            output = subprocess.check_output(  # nosec
                command,
                stdin=None,
                stderr=None,
                timeout=TIMEOUT,
            )
            checksum = output.decode().split()[0]
            checksum_filename = output.decode().split()[1]
            logger.debug(f'Checksum for {checksum_filename} generated successfully: {checksum}')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)

        return checksum

    @staticmethod
    def upload_checksum_file(latest_release: dict[str, Any]):
        """Uploads a `checksum.txt` file to the latest release of the repo."""
        logger = woodchips.get(LOGGER_NAME)

        latest_release_id = latest_release['id']

        with open(CHECKSUM_FILE, 'rb') as filename:
            checksum_binary = filename.read()

        upload_url = f'https://uploads.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/{latest_release_id}/assets?name={CHECKSUM_FILE}'  # noqa
        headers = GITHUB_HEADERS
        headers['Content-Type'] = 'text/plain'

        try:
            _ = requests.post(
                upload_url,
                headers=headers,
                data=checksum_binary,
                timeout=TIMEOUT,
            )
            logger.info(f'checksum.txt uploaded successfully to {GITHUB_REPO}.')
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)
