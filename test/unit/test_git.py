import subprocess

import mock
import pytest
from homebrew_releaser.constants import SUBPROCESS_TIMEOUT
from homebrew_releaser.git import Git


@mock.patch('subprocess.check_output')
def test_setup(mock_subprocess):
    # TODO: Mock the subprocess better to ensure it does what it's supposed to
    homebrew_owner = 'Justintime50'
    homebrew_tap = 'homebrew-formulas'
    commit_email = 'user@example.com'
    Git.setup(homebrew_owner, commit_email, homebrew_owner, homebrew_tap)

    mock_subprocess.assert_called_once_with(
        (
            # TODO: replace `None` with a mocked GITHUB_TOKEN
            f'git clone --depth=2 https://None@github.com/{homebrew_owner}/{homebrew_tap}.git'
            f' && cd {homebrew_tap}'
            f' && git config user.name "{homebrew_owner}"'
            f' && git config user.email {commit_email}'
        ),
        stdin=None,
        stderr=None,
        shell=True,
        timeout=SUBPROCESS_TIMEOUT
    )


@mock.patch('subprocess.check_output', side_effect=subprocess.TimeoutExpired(cmd=subprocess.check_output, timeout=0.1))  # noqa
def test_setup_subprocess_timeout(mock_subprocess):
    homebrew_owner = 'Justintime50'
    homebrew_tap = 'homebrew-formulas'
    commit_email = 'user@example.com'
    with pytest.raises(SystemExit):
        Git.setup(homebrew_owner, commit_email, homebrew_owner, homebrew_tap)


@mock.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.check_output))  # noqa
def test_setup_process_error(mock_subprocess):
    homebrew_owner = 'Justintime50'
    homebrew_tap = 'homebrew-formulas'
    commit_email = 'user@example.com'
    with pytest.raises(SystemExit):
        Git.setup(homebrew_owner, commit_email, homebrew_owner, homebrew_tap)


@mock.patch('subprocess.check_output')
def test_add(mock_subprocess):
    # TODO: Mock the subprocess better to ensure it does what it's supposed to
    homebrew_tap = 'homebrew-formulas'

    Git.add(homebrew_tap)
    mock_subprocess.assert_called_once_with(
        (
            f'cd {homebrew_tap}'
            f' && git add .'
        ),
        stdin=None,
        stderr=None,
        shell=True,
        timeout=SUBPROCESS_TIMEOUT
    )


@mock.patch('subprocess.check_output', side_effect=subprocess.TimeoutExpired(cmd=subprocess.check_output, timeout=0.1))  # noqa
def test_add_subprocess_timeout(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'

    with pytest.raises(SystemExit):
        Git.add(homebrew_tap)


@mock.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.check_output))  # noqa
def test_add_process_error(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'

    with pytest.raises(SystemExit):
        Git.add(homebrew_tap)


@mock.patch('subprocess.check_output')
def test_commit(mock_subprocess):
    # TODO: Mock the subprocess better to ensure it does what it's supposed to
    homebrew_tap = 'homebrew-formulas'
    repo_name = 'mock-repo'
    version = '0.1.0'

    Git.commit(homebrew_tap, repo_name, version)
    mock_subprocess.assert_called_once_with(
        (
            f'cd {homebrew_tap}'
            f' && git commit -m "Brew formula update for {repo_name} version {version}"'
        ),
        stdin=None,
        stderr=None,
        shell=True,
        timeout=SUBPROCESS_TIMEOUT
    )


@mock.patch('subprocess.check_output', side_effect=subprocess.TimeoutExpired(cmd=subprocess.check_output, timeout=0.1))  # noqa
def test_commit_subprocess_timeout(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'
    repo_name = 'mock-repo'
    version = '0.1.0'

    with pytest.raises(SystemExit):
        Git.commit(homebrew_tap, repo_name, version)


@mock.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.check_output))  # noqa
def test_commit_process_error(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'
    repo_name = 'mock-repo'
    version = '0.1.0'

    with pytest.raises(SystemExit):
        Git.commit(homebrew_tap, repo_name, version)


@mock.patch('subprocess.check_output')
def test_push(mock_subprocess):
    # TODO: Mock the subprocess better to ensure it does what it's supposed to
    homebrew_tap = 'homebrew-formulas'
    homebrew_owner = 'Justintime50'

    Git.push(homebrew_tap, homebrew_owner)
    mock_subprocess.assert_called_once_with(
        (
            f'cd {homebrew_tap}'
            # TODO: replace `None` with a mocked GITHUB_TOKEN
            f' && git push https://None@github.com/{homebrew_owner}/{homebrew_tap}.git'
        ),
        stdin=None,
        stderr=None,
        shell=True,
        timeout=SUBPROCESS_TIMEOUT
    )


@mock.patch('subprocess.check_output', side_effect=subprocess.TimeoutExpired(cmd=subprocess.check_output, timeout=0.1))  # noqa
def test_push_subprocess_timeout(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'
    homebrew_owner = 'Justintime50'

    with pytest.raises(SystemExit):
        Git.push(homebrew_tap, homebrew_owner)


@mock.patch('subprocess.check_output', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.check_output))  # noqa
def test_push_process_error(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'
    homebrew_owner = 'Justintime50'

    with pytest.raises(SystemExit):
        Git.push(homebrew_tap, homebrew_owner)
