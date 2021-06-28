import logging

import requests

from homebrew_releaser.constants import GITHUB_HEADERS


class Utils():
    @staticmethod
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

    @staticmethod
    def write_file(filename, content, mode='w'):
        """Writes content to a file
        """
        try:
            with open(filename, mode) as f:
                f.write(content)
            logging.debug(f'{filename} written successfully.')
        except Exception as error:
            raise SystemExit(error)
