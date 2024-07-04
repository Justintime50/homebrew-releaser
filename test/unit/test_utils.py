from unittest.mock import (
    mock_open,
    patch,
)

import pytest
import requests

from homebrew_releaser.constants import GITHUB_HEADERS
from homebrew_releaser.utils import Utils


@patch('requests.get')
def test_make_github_get_request(mock_request):
    url = 'https://api.github.com/repos/Justintime50/homebrew-releaser'
    Utils.make_github_get_request(url=url)

    mock_request.assert_called_once_with(
        url,
        headers=GITHUB_HEADERS,
        allow_redirects=True,
        stream=False,
        timeout=30,
    )


@patch('requests.get')
def test_make_github_get_request_stream(mock_request):
    """Tests that we setup a request correctly when we enable streaming."""
    url = 'https://api.github.com/repos/Justintime50/homebrew-releaser'
    Utils.make_github_get_request(url=url, stream=True)

    headers = GITHUB_HEADERS
    headers['Accept'] = 'application/octet-stream'

    mock_request.assert_called_once_with(
        url,
        headers=headers,
        allow_redirects=True,
        stream=True,
        timeout=30,
    )


@patch('requests.get', side_effect=requests.exceptions.RequestException('mock-error'))
def test_make_github_get_request_exception(mock_request):
    url = 'https://api.github.com/repos/Justintime50/homebrew-releaser'
    with pytest.raises(SystemExit) as error:
        Utils.make_github_get_request(url=url)

    assert 'mock-error' == str(error.value)


def test_write_file():
    with patch('builtins.open', mock_open()):
        Utils.write_file('mock-file', 'mock-content', mode='w')


def test_write_file_exception():
    with patch('builtins.open', mock_open()) as mock_open_file:
        mock_open_file.side_effect = Exception
        with pytest.raises(SystemExit):
            Utils.write_file('mock-file', 'mock-content', mode='w')


def test_get_filename_from_path():
    """Tests that we can pull the last part of a path out as a filename."""
    path = '/mock/path/to/filename.txt'
    filename = Utils.get_filename_from_path(path)

    assert filename == 'filename.txt'
