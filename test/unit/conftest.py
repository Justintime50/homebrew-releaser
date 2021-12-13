from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_tar_filename():
    return 'mock-file.tar.gz'


@pytest.fixture
def mock_git_repo():
    mock_git_repo = MagicMock()
    mock_git_repo.id = '123'
    mock_git_repo.name = 'mock-repo-name'

    return mock_git_repo
