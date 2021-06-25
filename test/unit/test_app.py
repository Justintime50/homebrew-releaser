import mock
from homebrew_releaser.app import App


@mock.patch('homebrew_releaser.utils.Utils.write_file')
@mock.patch('homebrew_releaser.utils.Utils.make_get_request')
def test_get_latest_tar_archive(mock_make_get_request, mock_write_file):
    url = 'https://api.github.com/repos/Justintime50/homebrew-releaser/archive/v0.1.0.tar.gz'
    App.get_latest_tar_archive(url)
    mock_make_get_request.assert_called_once_with(url, True)
    mock_write_file.assert_called_once()  # TODO: Assert `called_with` here instead
