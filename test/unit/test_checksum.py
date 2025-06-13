import subprocess
from unittest.mock import (
    mock_open,
    patch,
)

import pytest
import requests

from homebrew_releaser.checksum import Checksum


def test_get_checksum():
    """Tests that we can get the checksum of a file (we use one that will never change)."""
    checksum = Checksum.get_checksum('homebrew_releaser/__init__.py')

    assert checksum == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


@patch(
    'subprocess.check_output', side_effect=subprocess.CalledProcessError(returncode=1, cmd='subprocess.check_output')
)
def test_get_checksum_process_error(mock_subprocess, mock_tar_filename):
    with pytest.raises(SystemExit):
        Checksum.get_checksum(mock_tar_filename)


@patch('requests.post')
@patch('homebrew_releaser.utils.Utils.make_github_get_request')
def test_upload_checksum_file(mock_make_github_get_request, mock_post_request):
    """Tests that we make the GET call to retrieve the latest release and the
    POST call to upload the checksum.txt file.
    """
    with patch('builtins.open', mock_open()):
        Checksum.upload_checksum_file({'id': 1, 'tag_name': 'v1.0.0'})

        mock_post_request.assert_called_once()


@patch('requests.post', side_effect=requests.exceptions.RequestException('mock-error'))
@patch('homebrew_releaser.utils.Utils.make_github_get_request')
def test_upload_checksum_file_error_on_upload(mock_make_github_get_request, mock_post_request):
    """Tests that we exit on error to upload checksum.txt file."""
    with patch('builtins.open', mock_open()):
        with pytest.raises(SystemExit) as error:
            Checksum.upload_checksum_file({'id': 1, 'tag_name': 'v1.0.0'})

            mock_post_request.assert_called_once()

    assert 'mock-error' == str(error.value)
