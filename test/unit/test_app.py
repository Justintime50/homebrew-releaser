import mock
import pytest
from homebrew_releaser.app import App


@mock.patch('homebrew_releaser.app.SKIP_COMMIT', True)
@mock.patch('logging.info')
@mock.patch('homebrew_releaser.git.Git.setup')
@mock.patch('homebrew_releaser.git.Git.add')
@mock.patch('homebrew_releaser.git.Git.commit')
@mock.patch('homebrew_releaser.git.Git.push')
@mock.patch('homebrew_releaser.utils.Utils.write_file')
@mock.patch('homebrew_releaser.formula.Formula.generate_formula_data')
@mock.patch('homebrew_releaser.checksum.Checksum.get_checksum')
@mock.patch('homebrew_releaser.app.App.download_latest_tar_archive')
@mock.patch('homebrew_releaser.utils.Utils.make_get_request')
@mock.patch('homebrew_releaser.app.App.check_required_env_variables')
def test_run_github_action_skip_commit(mock_check_env_variables, mock_make_get_request,
                                       mock_download_latest_tar_archive, mock_get_checksum,
                                       mock_generate_formula, mock_write_file, mock_push_formula,
                                       mock_commit_formula, mock_add_formula, mock_setup_git,
                                       mock_logger):
    # TODO: Assert these `called_with` eventually
    App.run_github_action()
    assert mock_logger.call_count == 7
    mock_check_env_variables.assert_called_once()
    assert mock_make_get_request.call_count == 2
    mock_download_latest_tar_archive.assert_called_once()
    mock_get_checksum.assert_called_once()
    mock_generate_formula.assert_called_once()
    mock_write_file.assert_called_once()
    mock_setup_git.assert_called_once()
    mock_add_formula.assert_not_called()
    mock_commit_formula.assert_not_called()
    mock_push_formula.assert_not_called()


@mock.patch('logging.info')
@mock.patch('homebrew_releaser.git.Git.setup')
@mock.patch('homebrew_releaser.git.Git.add')
@mock.patch('homebrew_releaser.git.Git.commit')
@mock.patch('homebrew_releaser.git.Git.push')
@mock.patch('homebrew_releaser.utils.Utils.write_file')
@mock.patch('homebrew_releaser.formula.Formula.generate_formula_data')
@mock.patch('homebrew_releaser.checksum.Checksum.get_checksum')
@mock.patch('homebrew_releaser.app.App.download_latest_tar_archive')
@mock.patch('homebrew_releaser.utils.Utils.make_get_request')
@mock.patch('homebrew_releaser.app.App.check_required_env_variables')
def test_run_github_action(mock_check_env_variables, mock_make_get_request, mock_download_latest_tar_archive,
                           mock_get_checksum, mock_generate_formula, mock_write_file, mock_push_formula,
                           mock_commit_formula, mock_add_formula, mock_setup_git, mock_logger):
    # TODO: Assert these `called_with` eventually
    App.run_github_action()
    assert mock_logger.call_count == 8
    mock_check_env_variables.assert_called_once()
    assert mock_make_get_request.call_count == 2
    mock_download_latest_tar_archive.assert_called_once()
    mock_get_checksum.assert_called_once()
    mock_generate_formula.assert_called_once()
    mock_write_file.assert_called_once()
    mock_setup_git.assert_called_once()
    mock_add_formula.assert_called_once()
    mock_commit_formula.assert_called_once()
    mock_push_formula.assert_called_once()


@mock.patch('homebrew_releaser.app.GITHUB_TOKEN', '123')
@mock.patch('homebrew_releaser.app.HOMEBREW_OWNER', 'Justintime50')
@mock.patch('homebrew_releaser.app.HOMEBREW_TAP', 'homebrew-formulas')
@mock.patch('homebrew_releaser.app.INSTALL', 'bin.install "src/my-script.sh" => "my-script"')
@mock.patch('sys.exit')
def test_check_required_env_variables(mock_system_exit):
    App.check_required_env_variables()
    mock_system_exit.assert_not_called()


@mock.patch('sys.exit')
def test_check_required_env_variables_missing_env_variable(mock_system_exit):
    with pytest.raises(SystemExit) as error:
        App.check_required_env_variables()
        mock_system_exit.assert_called_once()
    assert str(error.value) == 'You must provide all necessary environment variables. Please reference the Homebrew Releaser documentation.'  # noqa


@mock.patch('homebrew_releaser.utils.Utils.write_file')
@mock.patch('homebrew_releaser.utils.Utils.make_get_request')
def test_download_latest_tar_archive(mock_make_get_request, mock_write_file):
    url = 'https://api.github.com/repos/Justintime50/homebrew-releaser/archive/v0.1.0.tar.gz'
    App.download_latest_tar_archive(url)
    mock_make_get_request.assert_called_once_with(url, True)
    mock_write_file.assert_called_once()  # TODO: Assert `called_with` here instead
