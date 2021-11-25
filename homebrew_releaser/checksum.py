import subprocess

import woodchips

from homebrew_releaser.constants import LOGGER_NAME, SUBPROCESS_TIMEOUT


class Checksum:
    @staticmethod
    def get_checksum(tar_filepath: str) -> str:
        """Gets the checksum of a file."""
        logger = woodchips.get(LOGGER_NAME)

        # TODO: Create and upload a `checksums.txt` file to the release for the zip and tar archives
        try:
            command = ['shasum', '-a', '256', tar_filepath]
            output = subprocess.check_output(
                command,
                stdin=None,
                stderr=None,
                timeout=SUBPROCESS_TIMEOUT,
            )
            checksum = output.decode().split()[0]
            checksum_file = output.decode().split()[1]  # TODO: Use this to craft the `checksums.txt` file  # noqa
            logger.debug(f'Checksum generated successfully: {checksum}')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)

        return checksum
