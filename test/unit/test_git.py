import subprocess
from unittest.mock import (
    call,
    patch,
)

import pytest

from homebrew_releaser.constants import TIMEOUT
from homebrew_releaser.git import Git


@patch('homebrew_releaser.git.GITHUB_TOKEN', '123')
@patch('subprocess.check_output')
def test_setup(mock_subprocess):
    homebrew_owner = 'Justintime50'
    homebrew_tap = 'homebrew-formulas'
    commit_email = 'user@example.com'
    Git.setup(homebrew_owner, commit_email, homebrew_owner, homebrew_tap)

    mock_subprocess.assert_has_calls(
        [
            call(
                [
                    'git',
                    'clone',
                    '--depth=1',
                    'https://x-access-token:123@github.com/Justintime50/homebrew-formulas.git',
                ],
                stdin=None,
                timeout=30,
            ),
            call(
                ['git', '-C', 'homebrew-formulas', 'config', 'user.name', '"Justintime50"'],
                stdin=None,
                timeout=30,
            ),
            call(
                ['git', '-C', 'homebrew-formulas', 'config', 'user.email', 'user@example.com'],
                stdin=None,
                timeout=30,
            ),
        ]
    )


@patch(
    'subprocess.check_output',
    side_effect=subprocess.TimeoutExpired(cmd='subprocess.check_output', timeout=0.1),
)
def test_setup_subprocess_timeout(mock_subprocess):
    homebrew_owner = 'Justintime50'
    homebrew_tap = 'homebrew-formulas'
    commit_email = 'user@example.com'
    with pytest.raises(subprocess.TimeoutExpired):
        Git.setup(homebrew_owner, commit_email, homebrew_owner, homebrew_tap)


@patch(
    'subprocess.check_output',
    side_effect=subprocess.CalledProcessError(cmd='subprocess.check_output', returncode=1),
)
def test_setup_process_error(mock_subprocess):
    homebrew_owner = 'Justintime50'
    homebrew_tap = 'homebrew-formulas'
    commit_email = 'user@example.com'
    with pytest.raises(subprocess.CalledProcessError):
        Git.setup(homebrew_owner, commit_email, homebrew_owner, homebrew_tap)


@patch('subprocess.check_output')
def test_add(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'

    Git.add(homebrew_tap)
    mock_subprocess.assert_called_once_with(
        ['git', '-C', homebrew_tap, 'add', '.'],
        stdin=None,
        timeout=TIMEOUT,
    )


@patch('subprocess.check_output', side_effect=subprocess.TimeoutExpired(cmd='subprocess.check_output', timeout=0.1))
def test_add_subprocess_timeout(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'

    with pytest.raises(subprocess.TimeoutExpired):
        Git.add(homebrew_tap)


@patch(
    'subprocess.check_output', side_effect=subprocess.CalledProcessError(cmd='subprocess.check_output', returncode=1)
)
def test_add_process_error(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'

    with pytest.raises(subprocess.CalledProcessError):
        Git.add(homebrew_tap)


@patch('subprocess.check_output')
def test_commit(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'
    repo_name = 'mock-repo'
    version = '0.1.0'

    Git.commit(homebrew_tap, repo_name, version)
    mock_subprocess.assert_called_once_with(
        ['git', '-C', homebrew_tap, 'commit', '-m', f'"Brew formula update for {repo_name} version {version}"'],
        stdin=None,
        timeout=TIMEOUT,
    )


@patch('subprocess.check_output', side_effect=subprocess.TimeoutExpired(cmd='subprocess.check_output', timeout=0.1))
def test_commit_subprocess_timeout(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'
    repo_name = 'mock-repo'
    version = '0.1.0'

    with pytest.raises(subprocess.TimeoutExpired):
        Git.commit(homebrew_tap, repo_name, version)


@patch(
    'subprocess.check_output', side_effect=subprocess.CalledProcessError(cmd='subprocess.check_output', returncode=1)
)
def test_commit_process_error(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'
    repo_name = 'mock-repo'
    version = '0.1.0'

    with pytest.raises(subprocess.CalledProcessError):
        Git.commit(homebrew_tap, repo_name, version)


@patch('homebrew_releaser.git.GITHUB_TOKEN', '123')
@patch('subprocess.check_output')
def test_push(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'
    homebrew_owner = 'Justintime50'

    Git.push(homebrew_tap, homebrew_owner)

    mock_subprocess.assert_called_once_with(
        [
            'git',
            '-C',
            homebrew_tap,
            'push',
            f'https://x-access-token:123@github.com/{homebrew_owner}/{homebrew_tap}.git',
        ],
        stdin=None,
        timeout=TIMEOUT,
    )


@patch('subprocess.check_output', side_effect=subprocess.TimeoutExpired(cmd='subprocess.check_output', timeout=0.1))
def test_push_subprocess_timeout(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'
    homebrew_owner = 'Justintime50'

    with pytest.raises(subprocess.TimeoutExpired):
        Git.push(homebrew_tap, homebrew_owner)


@patch(
    'subprocess.check_output', side_effect=subprocess.CalledProcessError(cmd='subprocess.check_output', returncode=1)
)
def test_push_process_error(mock_subprocess):
    homebrew_tap = 'homebrew-formulas'
    homebrew_owner = 'Justintime50'

    with pytest.raises(subprocess.CalledProcessError):
        Git.push(homebrew_tap, homebrew_owner)
