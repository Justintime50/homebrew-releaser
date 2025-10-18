import shutil
import subprocess  # nosec B404

import woodchips

from homebrew_releaser.constants import (
    LOGGER_NAME,
    TIMEOUT,
)


def update_python_resources(formula_dir: str, formula_filename: str) -> None:
    """Runs brew update-python-resources on the formula to add Python resources."""
    logger = woodchips.get(LOGGER_NAME)

    brew_path = shutil.which('brew')

    try:
        subprocess.check_output(
            f'cd {formula_dir} && {brew_path} update-python-resources {formula_filename}',
            stderr=subprocess.STDOUT,
            text=True,
            timeout=TIMEOUT,
            shell=True,  # nosec
        )
        logger.info('Updated Python resources successfully.')
    except subprocess.TimeoutExpired:
        raise SystemExit('Timed out updating Python resources')
    except subprocess.CalledProcessError as e:
        error_output = e.output if hasattr(e, "output") else ""

        raise SystemExit(f"An error occurred while updating Python resources: {error_output}")


def setup_homebrew_tap(homebrew_owner: str, homebrew_tap: str, formula_dir: str) -> None:
    """Sets up the Homebrew tap."""
    logger = woodchips.get(LOGGER_NAME)

    brew_path = shutil.which('brew')

    try:
        subprocess.check_output(
            f'{brew_path} tap {homebrew_owner}/{homebrew_tap} {formula_dir}/../',
            stderr=subprocess.STDOUT,
            text=True,
            timeout=TIMEOUT,
            shell=True,  # nosec
        )
        logger.info('Set up Homebrew tap successfully.')
    except subprocess.TimeoutExpired:
        raise SystemExit('Timed out setting up Homebrew tap')
    except subprocess.CalledProcessError as e:
        error_output = e.output if hasattr(e, "output") else ""

        raise SystemExit(f"An error occurred while setting up Homebrew tap: {error_output}")
