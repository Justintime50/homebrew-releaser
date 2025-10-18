import os
from unittest.mock import patch

from homebrew_releaser.app import run_github_action


@patch.dict(os.environ, {'INPUT_SKIP_COMMIT': 'false'})
@patch.dict(os.environ, {'INPUT_SKIP_COMMIT': 'false'})
@patch('homebrew_releaser.app.update_readme')
@patch('homebrew_releaser.app.upload_checksum_file')
@patch('homebrew_releaser.app.HOMEBREW_TAP', '123')
@patch('woodchips.get')
@patch('homebrew_releaser.app.setup_git')
@patch('homebrew_releaser.app.add_git')
@patch('homebrew_releaser.app.commit_git')
@patch('homebrew_releaser.app.push_git')
@patch('homebrew_releaser.app.write_file')
@patch('homebrew_releaser.app.generate_formula_data')
@patch('homebrew_releaser.app.calculate_checksum', return_value=('123', 'mock-repo'))
@patch('homebrew_releaser.app._download_archive')
@patch('homebrew_releaser.app.make_github_get_request')
@patch('homebrew_releaser.app._check_required_env_variables')
def test_run_github_action_string_false_config(
    mock_check_env_variables,
    mock_make_github_get_request,
    mock_download_archive,
    mock_calculate_checksum,
    mock_generate_formula,
    mock_write_file,
    mock_push_formula,
    mock_commit_formula,
    mock_add_formula,
    mock_setup_git,
    mock_logger,
    mock_upload_checksum_file,
    mock_update_readme,
):
    run_github_action()

    # Check that string false works by running git operations
    mock_add_formula.assert_called_once()
    mock_commit_formula.assert_called_once()
    mock_push_formula.assert_called_once()

    # Check that we don't update the README with a string false
    mock_update_readme.assert_not_called()
