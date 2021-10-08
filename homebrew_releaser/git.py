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
            command = (
                f'git clone --depth=2 https://{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git'
                f' && cd {homebrew_tap}'
                f' && git config user.name "{commit_owner}"'
                f' && git config user.email {commit_email}'
            )
            output = subprocess.check_output(
                command,
                stdin=None,
                stderr=None,
                shell=True,
                timeout=SUBPROCESS_TIMEOUT,
            )
            logging.debug('Git environment setup successfully.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)
        return output

    @staticmethod
    def add(homebrew_tap):
        """Adds assets to a git commit"""
        try:
            output = subprocess.check_output(
                f'cd {homebrew_tap} && git add .',
                stdin=None,
                stderr=None,
                shell=True,
                timeout=SUBPROCESS_TIMEOUT,
            )
            logging.debug('Assets added to git commit successfully.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)
        return output

    @staticmethod
    def commit(homebrew_tap, repo_name, version):
        """Commits assets to the Homebrew tap (repo)"""
        try:
            output = subprocess.check_output(
                f'cd {homebrew_tap} && git commit -m "Brew formula update for {repo_name} version {version}"',
                stdin=None,
                stderr=None,
                shell=True,
                timeout=SUBPROCESS_TIMEOUT,
            )
            logging.debug('Assets committed successfully.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)
        return output

    @staticmethod
    def push(homebrew_tap, homebrew_owner):
        """Pushes assets to the remote Homebrew tap (repo)"""
        try:
            output = subprocess.check_output(
                f'cd {homebrew_tap} && git push https://{GITHUB_TOKEN}@github.com/{homebrew_owner}/{homebrew_tap}.git',
                stdin=None,
                stderr=None,
                shell=True,
                timeout=SUBPROCESS_TIMEOUT,
            )
            logging.debug(f'Assets pushed successfully to {homebrew_tap}.')
        except subprocess.TimeoutExpired as error:
            raise SystemExit(error)
        except subprocess.CalledProcessError as error:
            raise SystemExit(error)
        return output
