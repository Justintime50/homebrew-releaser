import subprocess  # nosec
from typing import Optional

import woodchips

from homebrew_releaser.constants import (
    GITHUB_TOKEN,
    LOGGER_NAME,
    TIMEOUT,
)
from homebrew_releaser.utils import get_working_dir


def setup_git(commit_owner: str, commit_email: str, homebrew_owner: str, homebrew_tap: str):
    """Sets up the git environment we'll need to commit our changes to the homebrew tap.

    1) Clone the Homebrew tap repo
    2) Navigate to the repo on disk
    3) Set git config for the commit
    """
    logger = woodchips.get(LOGGER_NAME)

    commands = [
        [
            "git",
            "clone",
            "--depth=1",
            f"https://x-access-token:{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git",
            get_working_dir(homebrew_tap),
        ],
        ["git", "-C", get_working_dir(homebrew_tap), "config", "user.name", f'"{commit_owner}"'],
        ["git", "-C", get_working_dir(homebrew_tap), "config", "user.email", commit_email],
    ]

    for command in commands:
        _run_git_subprocess(command)

    logger.debug("Git environment setup successfully.")


def copy_to_git(formula_filepath: str, homebrew_tap: str):
    """Copies the formula from the official homebrew tap to the source code homebrew tap."""
    command = ["cp", formula_filepath, get_working_dir(homebrew_tap)]
    _run_git_subprocess(command, "Formula file moved to git successfully.")


def add_git(homebrew_tap: str):
    """Adds formula files to a git commit."""
    command = ["git", "-C", get_working_dir(homebrew_tap), "add", "*.rb"]
    _run_git_subprocess(command, "Formula file added to git commit successfully.")


def commit_git(homebrew_tap: str, repo_name: str, version: str):
    """Commits the formula file to the Homebrew tap repo."""
    # fmt: off
    command = ['git', '-C', get_working_dir(homebrew_tap), 'commit', '-m', f'chore: brew formula update for {repo_name} {version}']  # noqa
    # fmt: on
    _run_git_subprocess(command, "Formula file committed successfully.")


def push_git(homebrew_tap: str, homebrew_owner: str):
    """Pushes the formula file to the remote Homebrew tap repo."""
    # fmt: off
    command = ['git', '-C', get_working_dir(homebrew_tap), 'push', f'https://x-access-token:{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git']  # noqa
    # fmt: on
    _run_git_subprocess(command, f"Formula file pushed successfully to {homebrew_tap}.")


def _run_git_subprocess(command: list[str], debug_message: Optional[str] = None):
    """Runs a git subprocess."""
    logger = woodchips.get(LOGGER_NAME)

    try:
        subprocess.check_output(  # nosec
            command,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=TIMEOUT,
        )
        if debug_message:
            logger.debug(debug_message)
    except subprocess.CalledProcessError as error:
        logger.critical(error.output)
        raise
    except Exception as error:
        logger.critical(error)
        raise
