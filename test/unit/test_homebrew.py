import shutil
import subprocess  # nosec B404
from unittest.mock import patch

import pytest

from homebrew_releaser.homebrew import (
    setup_homebrew_tap,
    update_python_resources,
)


@patch('shutil.which', return_value='/usr/local/bin/brew')
@patch(
    'subprocess.check_output',
    side_effect=subprocess.CalledProcessError(cmd='subprocess.check_output', returncode=1),
)
def test_update_python_resources_error(mock_subprocess, mock_which):
    FORMULA_PATH = '/homebrew-formulas/Formula'
    formula_name = 'test-formula.rb'

    with pytest.raises(SystemExit):
        update_python_resources(FORMULA_PATH, formula_name)

    brew_path = shutil.which('brew')
    mock_subprocess.assert_called_once_with(
        f'cd {FORMULA_PATH} && {brew_path} update-python-resources {formula_name}',
        stderr=subprocess.STDOUT,
        text=True,
        timeout=300,
        shell=True,
    )


@patch('shutil.which', return_value='/usr/local/bin/brew')
@patch(
    'subprocess.check_output',
    side_effect=subprocess.CalledProcessError(cmd='subprocess.check_output', returncode=1),
)
def test_setup_homebrew_tap_error(mock_subprocess, mock_which):
    with pytest.raises(SystemExit):
        setup_homebrew_tap("owner", "tap", "dir")

    brew_path = shutil.which('brew')
    mock_subprocess.assert_called_once_with(
        f'{brew_path} tap owner/tap dir/../',
        stderr=subprocess.STDOUT,
        text=True,
        timeout=300,
        shell=True,
    )
