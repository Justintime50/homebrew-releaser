import os
import subprocess

import mock
import pytest
import requests
from homebrew_releaser.releaser import (GITHUB_HEADERS, SUBPROCESS_TIMEOUT,
                                        check_required_env_variables,
                                        commit_formula, generate_formula,
                                        get_checksum, get_latest_tar_archive,
                                        make_get_request, run_github_action,
                                        write_file)


@mock.patch('logging.info')
@mock.patch('homebrew_releaser.releaser.commit_formula')
@mock.patch('homebrew_releaser.releaser.write_file')
@mock.patch('homebrew_releaser.releaser.generate_formula')
@mock.patch('homebrew_releaser.releaser.get_checksum')
@mock.patch('homebrew_releaser.releaser.get_latest_tar_archive')
@mock.patch('homebrew_releaser.releaser.make_get_request')
@mock.patch('homebrew_releaser.releaser.check_required_env_variables')
def test_run_github_action(mock_check_env_variables, mock_make_get_request, mock_get_latest_tar_archive,
                           mock_get_checksum, mock_generate_formula, mock_write_file, mock_commit_formula,
                           mock_logger):
    # TODO: Assert these `called_with` eventually
    run_github_action()
    assert mock_logger.call_count == 6
    mock_check_env_variables.assert_called_once()
    assert mock_make_get_request.call_count == 2
    mock_get_latest_tar_archive.assert_called_once()
    mock_get_checksum.assert_called_once()
    mock_generate_formula.assert_called_once()
    mock_write_file.assert_called_once()
    mock_commit_formula.assert_called_once()


@mock.patch('homebrew_releaser.releaser.SKIP_COMMIT', True)
@mock.patch('logging.info')
@mock.patch('homebrew_releaser.releaser.commit_formula')
@mock.patch('homebrew_releaser.releaser.write_file')
@mock.patch('homebrew_releaser.releaser.generate_formula')
@mock.patch('homebrew_releaser.releaser.get_checksum')
@mock.patch('homebrew_releaser.releaser.get_latest_tar_archive')
@mock.patch('homebrew_releaser.releaser.make_get_request')
@mock.patch('homebrew_releaser.releaser.check_required_env_variables')
def test_run_github_action_skip_commit(mock_check_env_variables, mock_make_get_request, mock_get_latest_tar_archive,
                                       mock_get_checksum, mock_generate_formula, mock_write_file, mock_commit_formula,
                                       mock_logger):
    # TODO: Assert these `called_with` eventually
    run_github_action()
    assert mock_logger.call_count == 5
    mock_check_env_variables.assert_called_once()
    assert mock_make_get_request.call_count == 2
    mock_get_latest_tar_archive.assert_called_once()
    mock_get_checksum.assert_called_once()
    mock_generate_formula.assert_called_once()
    mock_write_file.assert_called_once()
    mock_commit_formula.assert_not_called()


@mock.patch('homebrew_releaser.releaser.HOMEBREW_OWNER', 'Justintime50')
@mock.patch('homebrew_releaser.releaser.HOMEBREW_TAP', 'homebrew-formulas')
@mock.patch('homebrew_releaser.releaser.INSTALL', 'bin.install "src/my-script.sh" => "my-script"')
@mock.patch('homebrew_releaser.releaser.GITHUB_TOKEN', '123')
@mock.patch('sys.exit')
def test_check_required_env_variables(mock_system_exit):
    check_required_env_variables()
    mock_system_exit.assert_not_called()


@mock.patch('sys.exit')
def test_check_required_env_variables_missing_env_variable(mock_system_exit):
    with pytest.raises(SystemExit) as error:
        check_required_env_variables()
        mock_system_exit.assert_called_once()
    assert str(error.value) == 'You must provide all necessary environment variables. Please reference the Homebrew Releaser documentation.'  # noqa


@mock.patch('requests.get')
def test_make_get_request(mock_request):
    url = 'https://api.github.com/repos/Justintime50/homebrew-releaser'
    make_get_request(url, False)
    mock_request.assert_called_once_with(url, headers=GITHUB_HEADERS, stream=False)


@mock.patch('requests.get', side_effect=requests.exceptions.RequestException('mock-error'))
def test_make_get_request_exception(mock_request):
    url = 'https://api.github.com/repos/Justintime50/homebrew-releaser'
    with pytest.raises(SystemExit):
        make_get_request(url, False)


@mock.patch('homebrew_releaser.releaser.write_file')
@mock.patch('homebrew_releaser.releaser.make_get_request')
def test_get_latest_tar_archive(mock_make_get_request, mock_write_file):
    url = 'https://api.github.com/repos/Justintime50/homebrew-releaser/archive/v0.1.0.tar.gz'
    get_latest_tar_archive(url)
    mock_make_get_request.assert_called_once_with(url, True)
    mock_write_file.assert_called_once()  # TODO: Assert `called_with` here instead


def test_write_file():
    with mock.patch('builtins.open', mock.mock_open()):
        write_file('mock-file', 'mock-content', mode='w')


def test_write_file_exception():
    with mock.patch('builtins.open', mock.mock_open()) as mock_open:
        mock_open.side_effect = Exception
        with pytest.raises(SystemExit):
            write_file('mock-file', 'mock-content', mode='w')


@mock.patch('subprocess.check_output')
def test_get_checksum(mock_subprocess):
    # TODO: Mock the subprocess better to ensure it does what it's supposed to
    mock_tar_file = 'mock-file.tar.gz'
    get_checksum(mock_tar_file)
    mock_subprocess.assert_called_once_with(
        f'shasum -a 256 {mock_tar_file}',
        stdin=None,
        stderr=None,
        shell=True,
        timeout=SUBPROCESS_TIMEOUT
    )


@mock.patch('subprocess.check_output', side_effect=subprocess.TimeoutExpired(cmd=subprocess.check_output, timeout=0.1))  # noqa
def test_get_checksum_subprocess_timeout(mock_subprocess):
    mock_tar_file = 'mock-file.tar.gz'
    with pytest.raises(SystemExit):
        get_checksum(mock_tar_file)


@mock.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.check_output))  # noqa
def test_get_checksum_process_error(mock_subprocess):
    mock_tar_file = 'mock-file.tar.gz'
    with pytest.raises(SystemExit):
        get_checksum(mock_tar_file)


def test_generate_formula():
    """This test generates the formula "cassette" file if it does not exist already
    To regenerate the file (when changes are made to how formula are generated), simply
    delete the file and run tests again. Ensure the output of the file is correct.
    """
    username = 'Justintime50'
    repo_name = 'homebrew-releaser'
    version = 'v0.1.0'
    repository = {
        'description': 'A tool to release... scripts, binaries, and executables to GitHub. ',
        'license': {
            'spdx_id': 'MIT'
        }
    }
    checksum = '1234567890123456789012345678901234567890'
    install = 'bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"'
    tar_url = f'https://github.com/{username}/{repo_name}/archive/{version}.tar.gz'
    test = None

    formula = generate_formula(username, repo_name, version, repository, checksum, install, tar_url, test)
    template_filename = 'test/unit/test_formula_template.rb.txt'

    # Read from existing file or create new file if it's not present
    if os.path.isfile(template_filename):
        with open(template_filename, 'r') as template_file:
            assert formula == template_file.read()
    else:
        with open(template_filename, 'w') as template_file:
            template_file.write(formula)


@mock.patch('subprocess.check_output')
def test_commit_formula(mock_subprocess):
    # TODO: Mock the subprocess better to ensure it does what it's supposed to
    commit_owner = 'Justintime50'
    commit_email = 'justin@example.com'
    homebrew_owner = 'Justintime50'
    homebrew_tap = 'homebrew-formulas'
    formula_folder = 'formula'
    repo_name = 'repo-name'
    version = 'v0.1.0'
    commit_formula(commit_owner, commit_email, homebrew_owner, homebrew_tap, formula_folder, repo_name, version)
    mock_subprocess.assert_called_once()  # TODO: Should we assert a `called_with` here since it's SO long?


@mock.patch('subprocess.check_output', side_effect=subprocess.TimeoutExpired(cmd=subprocess.check_output, timeout=0.1))  # noqa
def test_commit_formula_subprocess_timeout(mock_subprocess):
    commit_owner = 'Justintime50'
    commit_email = 'justin@example.com'
    homebrew_owner = 'Justintime50'
    homebrew_tap = 'homebrew-formulas'
    formula_folder = 'formula'
    repo_name = 'repo-name'
    version = 'v0.1.0'
    with pytest.raises(SystemExit):
        commit_formula(commit_owner, commit_email, homebrew_owner, homebrew_tap, formula_folder, repo_name, version)


@mock.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.check_output))  # noqa
def test_commit_formula_process_error(mock_subprocess):
    commit_owner = 'Justintime50'
    commit_email = 'justin@example.com'
    homebrew_owner = 'Justintime50'
    homebrew_tap = 'homebrew-formulas'
    formula_folder = 'formula'
    repo_name = 'repo-name'
    version = 'v0.1.0'
    with pytest.raises(SystemExit):
        commit_formula(commit_owner, commit_email, homebrew_owner, homebrew_tap, formula_folder, repo_name, version)
