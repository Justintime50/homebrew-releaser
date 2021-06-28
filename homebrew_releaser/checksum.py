import logging
import subprocess

from homebrew_releaser.constants import SUBPROCESS_TIMEOUT


class Checksum():
    @staticmethod
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
