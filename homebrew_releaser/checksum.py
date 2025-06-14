import hashlib
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
from homebrew_releaser.utils import Utils


class Checksum:
    @staticmethod
    def get_checksum(tar_filepath: str) -> str:
        """Gets the checksum of a file."""
        logger = woodchips.get(LOGGER_NAME)

        try:
            with open(Utils.get_working_dir(tar_filepath), "rb") as content:
                checksum = hashlib.sha256(content.read()).hexdigest()
            logger.debug(f'Checksum for {tar_filepath} generated successfully: {checksum}')
        except Exception as error:
            raise SystemExit(error)

        return checksum

    @staticmethod
    def upload_checksum_file(latest_release: dict[str, Any]):
        """Uploads a `checksum.txt` file to the latest release of the repo."""
        logger = woodchips.get(LOGGER_NAME)

        latest_release_id = latest_release['id']

        with open(Utils.get_working_dir(CHECKSUM_FILE), 'rb') as filename:
            checksum_file_content = filename.read()

        upload_url = f'https://uploads.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/{latest_release_id}/assets?name={CHECKSUM_FILE}'  # noqa
        headers = GITHUB_HEADERS.copy()
        headers['Content-Type'] = 'text/plain'

        try:
            response = requests.post(
                upload_url,
                headers=headers,
                data=checksum_file_content,
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            logger.info(f'checksum.txt uploaded successfully to {GITHUB_REPO}.')
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)
