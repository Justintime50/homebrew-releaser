from typing import Optional

import requests
import woodchips

from homebrew_releaser.constants import (
    GITHUB_HEADERS,
    LOGGER_NAME,
    TIMEOUT,
)


class Utils:
    @staticmethod
    def make_github_get_request(url: str, stream: Optional[bool] = False) -> requests.Response:
        """Make an HTTP GET request."""
        logger = woodchips.get(LOGGER_NAME)

        headers = GITHUB_HEADERS
        if stream:
            headers['Accept'] = 'application/octet-stream'

        try:
            response = requests.get(
                url,
                headers=headers,
                allow_redirects=True,  # We need to allow redirects to reach various GitHub resources
                stream=stream,
                timeout=TIMEOUT,
            )
            response.raise_for_status()
            logger.debug(f'HTTP GET request made successfully to {url}.')
        except Exception as error:
            raise SystemExit(error)

        return response

    @staticmethod
    def write_file(file_path: str, content: str | bytes, mode: str = 'w'):
        """Writes content to a file."""
        logger = woodchips.get(LOGGER_NAME)

        try:
            with open(file_path, mode) as f:
                f.write(content)
            logger.debug(f'{file_path} written successfully.')
        except Exception as error:
            raise SystemExit(error)

    @staticmethod
    def get_filename_from_path(path: str) -> str:
        """Gets the last part of a path (the filename)."""
        return path.rsplit('/', 1)[1]
