import pytest


@pytest.fixture
def mock_tar_filename():
    return 'mock-file.tar.gz'


@pytest.fixture
def mock_git_repo():
    mock_git_repo = {
        'id': '123',
        'name': 'mock-repo-name',
    }

    return mock_git_repo
