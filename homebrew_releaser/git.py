import subprocess  # nosec

import woodchips

from homebrew_releaser.constants import (
    GITHUB_TOKEN,
    LOGGER_NAME,
    TIMEOUT,
)


class Git:
    @staticmethod
    def setup(commit_owner: str, commit_email: str, homebrew_owner: str, homebrew_tap: str):
        """Sets up the git environment we'll need to commit our changes to the
        homebrew tap.

        1) Clone the Homebrew tap repo
        2) Navigate to the repo on disk
        3) Set git config for the commit
        """
        logger = woodchips.get(LOGGER_NAME)

        try:
            commands = [
                [
                    'git',
                    'clone',
                    '--depth=1',
                    f'https://x-access-token:{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git',
                ],
                ['git', '-C', homebrew_tap, 'config', 'user.name', f'"{commit_owner}"'],
                ['git', '-C', homebrew_tap, 'config', 'user.email', commit_email],
            ]

            for command in commands:
                subprocess.check_output(  # nosec
                    command,
                    stdin=None,
                    stderr=None,
                    timeout=TIMEOUT,
                )
            logger.debug('Git environment setup successfully.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)

    @staticmethod
    def add(homebrew_tap: str):
        """Adds assets to a git commit."""
        logger = woodchips.get(LOGGER_NAME)

        try:
            command = ['git', '-C', homebrew_tap, 'add', '.']
            subprocess.check_output(  # nosec
                command,
                stdin=None,
                stderr=None,
                timeout=TIMEOUT,
            )
            logger.debug('Assets added to git commit successfully.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)

    @staticmethod
    def commit(homebrew_tap: str, repo_name: str, version: str):
        """Commits assets to the Homebrew tap (repo)."""
        logger = woodchips.get(LOGGER_NAME)

        try:
            # fmt: off
            command = ['git', '-C', homebrew_tap, 'commit', '-m', f'"Brew formula update for {repo_name} version {version}"']  # noqa
            # fmt: on
            subprocess.check_output(  # nosec
                command,
                stdin=None,
                stderr=None,
                timeout=TIMEOUT,
            )
            logger.debug('Assets committed successfully.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)

    @staticmethod
    def push(homebrew_tap: str, homebrew_owner: str):
        """Pushes assets to the remote Homebrew tap (repo)."""
        logger = woodchips.get(LOGGER_NAME)

        try:
            # fmt: off
            command = ['git', '-C', homebrew_tap, 'push', f'https://x-access-token:{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git']  # noqa
            # fmt: on
            subprocess.check_output(  # nosec
                command,
                stdin=None,
                stderr=None,
                timeout=TIMEOUT,
            )
            logger.debug(f'Assets pushed successfully to {homebrew_tap}.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)
