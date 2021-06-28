import mock
import pytest
import requests
from homebrew_releaser.constants import GITHUB_HEADERS
from homebrew_releaser.utils import Utils


@mock.patch('requests.get')
def test_make_get_request(mock_request):
    url = 'https://api.github.com/repos/Justintime50/homebrew-releaser'
    Utils.make_get_request(url, False)
    mock_request.assert_called_once_with(url, headers=GITHUB_HEADERS, stream=False)


@mock.patch('requests.get', side_effect=requests.exceptions.RequestException('mock-error'))
def test_make_get_request_exception(mock_request):
    url = 'https://api.github.com/repos/Justintime50/homebrew-releaser'
    with pytest.raises(SystemExit):
        Utils.make_get_request(url, False)


def test_write_file():
    with mock.patch('builtins.open', mock.mock_open()):
        Utils.write_file('mock-file', 'mock-content', mode='w')


def test_write_file_exception():
    with mock.patch('builtins.open', mock.mock_open()) as mock_open:
        mock_open.side_effect = Exception
        with pytest.raises(SystemExit):
            Utils.write_file('mock-file', 'mock-content', mode='w')
