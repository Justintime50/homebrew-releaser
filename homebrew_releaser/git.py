import os
import subprocess  # nosec
from typing import Optional

import woodchips

from homebrew_releaser.constants import (
    FORMULA_FOLDER,
    GITHUB_TOKEN,
    LOGGER_NAME,
    TIMEOUT,
)
from homebrew_releaser.utils import build_dir_path


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
            build_dir_path(homebrew_tap),
        ],
        ["git", "-C", build_dir_path(homebrew_tap), "config", "user.name", f'"{commit_owner}"'],
        ["git", "-C", build_dir_path(homebrew_tap), "config", "user.email", commit_email],
    ]

    for command in commands:
        _run_git_subprocess(command)

    logger.debug("Git environment setup successfully.")


def make_formula_folder(homebrew_tap: str):
    """Makes the formula folder in the git repo if it does not already exist."""
    formula_folder_path = build_dir_path(homebrew_tap, FORMULA_FOLDER)

    if not os.path.exists(formula_folder_path):
        os.makedirs(formula_folder_path)


def copy_formula_file_to_git(formula_filepath: str, homebrew_tap: str):
    """Copies the formula file from the official homebrew tap to the source code homebrew tap."""
    command = ["cp", formula_filepath, build_dir_path(homebrew_tap, FORMULA_FOLDER)]
    _run_git_subprocess(command, "Formula file moved to git repo successfully.")


def add_git(homebrew_tap: str):
    """Adds git assets to a git commit."""
    # We add everything here because we updated the formula file and optionally the README
    command = ["git", "-C", build_dir_path(homebrew_tap), "add", "."]
    _run_git_subprocess(command, "Assets added to git commit successfully.")


def commit_git(homebrew_tap: str, repo_name: str, version: str):
    """Commits git assets to the Homebrew tap repo."""
    logger = woodchips.get(LOGGER_NAME)
    # fmt: off
    command = ['git', '-C', build_dir_path(homebrew_tap), 'commit', '-m', f'chore: brew formula update for {repo_name} {version}']  # noqa
    # fmt: on
    try:
        _run_git_subprocess(command, "Assets committed successfully.")
    except subprocess.CalledProcessError as e:
        if "nothing to commit" in e.output:
            logger.warning("No changes to commit.")
        else:
            raise


def push_git(homebrew_tap: str, homebrew_owner: str, branch: Optional[str] = None):
    """Pushes git assets to the remote Homebrew tap repo."""
    # fmt: off
    if branch:
        command = ['git', '-C', build_dir_path(homebrew_tap), 'push', f'https://x-access-token:{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git', f"HEAD:{branch}"]  # noqa
    else:
        command = ['git', '-C', build_dir_path(homebrew_tap), 'push', f'https://x-access-token:{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git']  # noqa
    # fmt: on
    _run_git_subprocess(command, f"Assets pushed successfully to {homebrew_tap}.")


def _run_git_subprocess(command: list[str], debug_message: Optional[str] = None):
    """Runs a git subprocess."""
    logger = woodchips.get(LOGGER_NAME)

    subprocess.check_output(  # nosec
        command,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=TIMEOUT,
    )
    if debug_message:
        logger.debug(debug_message)
