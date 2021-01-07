import subprocess

import mock
import pytest
import requests
from homebrew_releaser.releaser import (HEADERS, SUBPROCESS_TIMEOUT,
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
                           mock_get_checksum, mock_generate_formula, mock_write_file, mock_commit_fomrula,
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
    mock_commit_fomrula.assert_called_once()


@mock.patch('homebrew_releaser.releaser.HOMEBREW_FORMULA_FOLDER', 'formula')
@mock.patch('homebrew_releaser.releaser.HOMEBREW_TAP', 'homebrew-formulas')
@mock.patch('homebrew_releaser.releaser.INSTALL', '"bin.install \"src/my-script.sh\" => \"my-script\""')
@mock.patch('homebrew_releaser.releaser.REPO', 'homebrew-releaser')
@mock.patch('homebrew_releaser.releaser.OWNER', 'Justintime50')
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
    assert str(error.value) == 'You must provide all necessary environment variables. Please reference the documentation.'  # noqa


@mock.patch('requests.get')
def test_make_get_request(mock_request):
    url = 'https://api.github.com/repos/Justintime50/homebrew-releaser'
    make_get_request(url, False)
    mock_request.assert_called_once_with(url, headers=HEADERS, stream=False)


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
    username = 'Justintime50'
    repo_name = 'homebrew-releaser'
    version = 'v0.1.0'
    repository = {
        'description': 'Release scripts, binaries, and executables directly to Homebrew via GitHub Actions.',
        'license': {
            'spdx_id': 'MIT'
        }
    }
    checksum = '1234567890'
    install = 'bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"'
    tar_url = 'https://github.com/Justintime50/homebrew-releaser/archive/v0.1.0.tar.gz'
    test = None

    formula = generate_formula(username, repo_name, version, repository, checksum, install, tar_url, test)
    assert formula == f"""# typed: false
# frozen_string_literal: true

# This file was generated by Homebrew Releaser. DO NOT EDIT.
class HomebrewReleaser < Formula
  desc "Release scripts, binaries, and executables directly to Homebr"
  homepage "https://github.com/{username}/{repo_name}"
  url "{tar_url}"
  sha256 "{checksum}"
  license "{repository['license']['spdx_id']}"
  bottle :unneeded

  def install
    {install}
  end
end
"""


@mock.patch('subprocess.check_output')
def test_commit_formula(mock_subprocess):
    # TODO: Mock the subprocess better to ensure it does what it's supposed to
    owner = 'Justintime50'
    owner_email = 'justin@example.com'
    repo = 'repo-name'
    version = 'v0.1.0'
    commit_formula(owner, owner_email, repo, version)
    mock_subprocess.assert_called_once()  # TODO: Should we assert a `called_with` here since it's SO long?


@mock.patch('subprocess.check_output', side_effect=subprocess.TimeoutExpired(cmd=subprocess.check_output, timeout=0.1))  # noqa
def test_commit_formula_subprocess_timeout(mock_subprocess):
    owner = 'Justintime50'
    owner_email = 'justin@example.com'
    repo = 'repo-name'
    version = 'v0.1.0'
    with pytest.raises(SystemExit):
        commit_formula(owner, owner_email, repo, version)


@mock.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.check_output))  # noqa
def test_commit_formula_process_error(mock_subprocess):
    owner = 'Justintime50'
    owner_email = 'justin@example.com'
    repo = 'repo-name'
    version = 'v0.1.0'
    with pytest.raises(SystemExit):
        commit_formula(owner, owner_email, repo, version)
