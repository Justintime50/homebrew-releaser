from typing import Optional

import requests
import woodchips

from homebrew_releaser.constants import (
    GITHUB_HEADERS,
    LOGGER_NAME,
)


class Utils:
    @staticmethod
    def make_get_request(url: str, stream: Optional[bool] = False) -> requests.Response:
        """Make an HTTP GET request."""
        logger = woodchips.get(LOGGER_NAME)

        try:
            response = requests.get(
                url,
                headers=GITHUB_HEADERS,
                stream=stream,
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
