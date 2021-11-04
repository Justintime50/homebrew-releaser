import logging
import subprocess

from homebrew_releaser.constants import GITHUB_TOKEN, SUBPROCESS_TIMEOUT


class Git:
    @staticmethod
    def setup(commit_owner, commit_email, homebrew_owner, homebrew_tap):
        """Sets up the git environment we'll need to commit our changes to the
        homebrew tap.

        1) Clone the Homebrew tap repo
        2) Navigate to the repo on disk
        3) Set git config for the commit
        """
        try:
            commands = [
                ['git', 'clone', '--depth=1', f'https://{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git'],
                ['git', '-C', homebrew_tap, 'config', 'user.name', f'"{commit_owner}"'],
                ['git', '-C', homebrew_tap, 'config', 'user.email', commit_email],
            ]

            for command in commands:
                subprocess.check_output(
                    command,
                    stdin=None,
                    stderr=None,
                    timeout=SUBPROCESS_TIMEOUT,
                )
            logging.debug('Git environment setup successfully.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)

    @staticmethod
    def add(homebrew_tap):
        """Adds assets to a git commit"""
        try:
            command = ['git', '-C', homebrew_tap, 'add', '.']
            subprocess.check_output(
                command,
                stdin=None,
                stderr=None,
                timeout=SUBPROCESS_TIMEOUT,
            )
            logging.debug('Assets added to git commit successfully.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)

    @staticmethod
    def commit(homebrew_tap, repo_name, version):
        """Commits assets to the Homebrew tap (repo)"""
        try:
            # fmt: off
            command = ['git', '-C', homebrew_tap, 'commit', '-m', f'"Brew formula update for {repo_name} version {version}"']  # noqa
            # fmt: on
            subprocess.check_output(
                command,
                stdin=None,
                stderr=None,
                timeout=SUBPROCESS_TIMEOUT,
            )
            logging.debug('Assets committed successfully.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)

    @staticmethod
    def push(homebrew_tap, homebrew_owner):
        """Pushes assets to the remote Homebrew tap (repo)"""
        try:
            # fmt: off
            command = ['git', '-C', homebrew_tap, 'push', f'https://{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git']  # noqa
            # fmt: on
            subprocess.check_output(
                command,
                stdin=None,
                stderr=None,
                timeout=SUBPROCESS_TIMEOUT,
            )
            logging.debug(f'Assets pushed successfully to {homebrew_tap}.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)
