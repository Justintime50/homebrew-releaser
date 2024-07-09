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
    """Tests that we call the correct subprocess commands when setting up the git environment."""
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
                stderr=-2,
                text=True,
                timeout=30,
            ),
            call(
                ['git', '-C', 'homebrew-formulas', 'config', 'user.name', '"Justintime50"'],
                stderr=-2,
                text=True,
                timeout=30,
            ),
            call(
                ['git', '-C', 'homebrew-formulas', 'config', 'user.email', 'user@example.com'],
                stderr=-2,
                text=True,
                timeout=30,
            ),
        ]
    )


@patch('subprocess.check_output')
def test_add(mock_subprocess):
    """Tests that we call the correct git add command."""
    homebrew_tap = 'homebrew-formulas'

    Git.add(homebrew_tap)
    mock_subprocess.assert_called_once_with(
        ['git', '-C', homebrew_tap, 'add', '.'],
        stderr=-2,
        text=True,
        timeout=TIMEOUT,
    )


@patch('subprocess.check_output')
def test_commit(mock_subprocess):
    """Tests that we call the correct git commit command."""
    homebrew_tap = 'homebrew-formulas'
    repo_name = 'mock-repo'
    version = '0.1.0'

    Git.commit(homebrew_tap, repo_name, version)
    mock_subprocess.assert_called_once_with(
        ['git', '-C', homebrew_tap, 'commit', '-m', f'chore: brew formula update for {repo_name} {version}'],
        stderr=-2,
        text=True,
        timeout=TIMEOUT,
    )


@patch('homebrew_releaser.git.GITHUB_TOKEN', '123')
@patch('subprocess.check_output')
def test_push(mock_subprocess):
    """Tests that we call the correct git push command."""
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
        stderr=-2,
        text=True,
        timeout=TIMEOUT,
    )


@patch('logging.Logger.debug')
@patch(
    'subprocess.check_output',
    side_effect=subprocess.CalledProcessError(cmd='subprocess.check_output', returncode=1),
)
def test_setup_called_process_error(mock_subprocess, mock_logger):
    """Tests that we log a subprocess error when they happen.

    All git commands should fail in the same manner.
    """
    homebrew_owner = 'Justintime50'
    homebrew_tap = 'homebrew-formulas'
    commit_email = 'user@example.com'
    with pytest.raises(subprocess.CalledProcessError):
        Git.setup(homebrew_owner, commit_email, homebrew_owner, homebrew_tap)

    mock_logger.assert_not_called()


@patch('logging.Logger.debug')
@patch(
    'subprocess.check_output',
    side_effect=Exception(),
)
def test_setup_exception(mock_subprocess, mock_logger):
    """Tests that we log an exception when they happen.

    All git commands should fail in the same manner.
    """
    homebrew_owner = 'Justintime50'
    homebrew_tap = 'homebrew-formulas'
    commit_email = 'user@example.com'
    with pytest.raises(Exception):
        Git.setup(homebrew_owner, commit_email, homebrew_owner, homebrew_tap)

    mock_logger.assert_not_called()
