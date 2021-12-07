import subprocess
from unittest.mock import patch

import pytest

from homebrew_releaser.checksum import Checksum
from homebrew_releaser.constants import SUBPROCESS_TIMEOUT


@patch('subprocess.check_output')
def test_get_checksum(mock_subprocess, mock_tar_filename):
    # TODO: Mock the subprocess better to ensure it does what it's supposed to
    Checksum.get_checksum(mock_tar_filename)

    mock_subprocess.assert_called_once_with(
        ['shasum', '-a', '256', mock_tar_filename],
        stdin=None,
        stderr=None,
        timeout=SUBPROCESS_TIMEOUT,
    )


@patch('subprocess.check_output', side_effect=subprocess.TimeoutExpired(cmd='subprocess.check_output', timeout=0.1))
def test_get_checksum_subprocess_timeout(mock_subprocess, mock_tar_filename):
    with pytest.raises(SystemExit):
        Checksum.get_checksum(mock_tar_filename)


@patch(
    'subprocess.check_output', side_effect=subprocess.CalledProcessError(returncode=1, cmd='subprocess.check_output')
)
def test_get_checksum_process_error(mock_subprocess, mock_tar_filename):
    with pytest.raises(SystemExit):
        Checksum.get_checksum(mock_tar_filename)
