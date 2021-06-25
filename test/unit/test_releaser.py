# import os
# import subprocess

# import mock
# import pytest
# import requests
# from homebrew_releaser.releaser import Releaser

# from homebrew_releaser.releaser import (GITHUB_HEADERS, SUBPROCESS_TIMEOUT,
#                                         check_required_env_variables,
#                                         commit_formula, generate_formula,
#                                         get_checksum, get_latest_tar_archive,
#                                         make_get_request, run_github_action,
#                                         write_file)


# @mock.patch('logging.info')
# @mock.patch('homebrew_releaser.releaser.setup_git')
# @mock.patch('homebrew_releaser.releaser.commit_formula')
# @mock.patch('homebrew_releaser.releaser.write_file')
# @mock.patch('homebrew_releaser.releaser.generate_formula')
# @mock.patch('homebrew_releaser.releaser.get_checksum')
# @mock.patch('homebrew_releaser.releaser.get_latest_tar_archive')
# @mock.patch('homebrew_releaser.releaser.make_get_request')
# @mock.patch('homebrew_releaser.releaser.check_required_env_variables')
# def test_run_github_action(mock_check_env_variables, mock_make_get_request, mock_get_latest_tar_archive,
#                            mock_get_checksum, mock_generate_formula, mock_write_file, mock_commit_formula,
#                            mock_setup_git, mock_logger):
#     # TODO: Assert these `called_with` eventually
#     run_github_action()
#     assert mock_logger.call_count == 7
#     mock_check_env_variables.assert_called_once()
#     assert mock_make_get_request.call_count == 2
#     mock_get_latest_tar_archive.assert_called_once()
#     mock_get_checksum.assert_called_once()
#     mock_generate_formula.assert_called_once()
#     mock_write_file.assert_called_once()
#     mock_commit_formula.assert_called_once()


# @mock.patch('homebrew_releaser.releaser.SKIP_COMMIT', True)
# @mock.patch('logging.info')
# @mock.patch('homebrew_releaser.releaser.commit_formula')
# @mock.patch('homebrew_releaser.releaser.write_file')
# @mock.patch('homebrew_releaser.releaser.generate_formula')
# @mock.patch('homebrew_releaser.releaser.get_checksum')
# @mock.patch('homebrew_releaser.releaser.get_latest_tar_archive')
# @mock.patch('homebrew_releaser.releaser.make_get_request')
# @mock.patch('homebrew_releaser.releaser.check_required_env_variables')
# def test_run_github_action_skip_commit(mock_check_env_variables, mock_make_get_request, mock_get_latest_tar_archive,
#                                        mock_get_checksum, mock_generate_formula, mock_write_file, mock_commit_formula,
#                                        mock_logger):
#     # TODO: Assert these `called_with` eventually
#     run_github_action()
#     assert mock_logger.call_count == 5
#     mock_check_env_variables.assert_called_once()
#     assert mock_make_get_request.call_count == 2
#     mock_get_latest_tar_archive.assert_called_once()
#     mock_get_checksum.assert_called_once()
#     mock_generate_formula.assert_called_once()
#     mock_write_file.assert_called_once()
#     mock_commit_formula.assert_not_called()


# @mock.patch('homebrew_releaser.releaser.HOMEBREW_OWNER', 'Justintime50')
# @mock.patch('homebrew_releaser.releaser.HOMEBREW_TAP', 'homebrew-formulas')
# @mock.patch('homebrew_releaser.releaser.INSTALL', 'bin.install "src/my-script.sh" => "my-script"')
# @mock.patch('homebrew_releaser.releaser.GITHUB_TOKEN', '123')
# @mock.patch('sys.exit')
# def test_check_required_env_variables(mock_system_exit):
#     check_required_env_variables()
#     mock_system_exit.assert_not_called()


# @mock.patch('sys.exit')
# def test_check_required_env_variables_missing_env_variable(mock_system_exit):
#     with pytest.raises(SystemExit) as error:
#         check_required_env_variables()
#         mock_system_exit.assert_called_once()
#     assert str(error.value) == 'You must provide all necessary environment variables. Please reference the Homebrew Releaser documentation.'  # noqa
