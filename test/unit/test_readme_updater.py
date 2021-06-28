import mock
import pytest
from homebrew_releaser.readme_updater import ReadmeUpdater


@mock.patch('homebrew_releaser.readme_updater.ReadmeUpdater.format_formula_data')
@mock.patch('homebrew_releaser.readme_updater.ReadmeUpdater.generate_table')
@mock.patch('homebrew_releaser.readme_updater.ReadmeUpdater.retrieve_old_table')
@mock.patch('homebrew_releaser.readme_updater.ReadmeUpdater.read_current_readme')
@mock.patch('homebrew_releaser.readme_updater.ReadmeUpdater.replace_table_contents')
def test_update_readme(mock_replace_table_contents, mock_read_current_readme,
                       mock_retrieve_old_table, mock_generate_table, mock_format_formula_data):
    ReadmeUpdater.update_readme('./')

    mock_format_formula_data.assert_called_once()
    mock_generate_table.assert_called_once()
    mock_retrieve_old_table.assert_called_once()
    mock_read_current_readme.assert_called_once()
    mock_read_current_readme.assert_called_once


# TODO: Add a test that formats the data
def test_format_formula_data_not_found():
    with pytest.raises(FileNotFoundError):
        ReadmeUpdater.format_formula_data('./')


def test_generate_table():
    # TODO: Format data here first
    # ReadmeUpdater.generate_table()
    pass


# TODO: Add another test with a table in the README
def test_retrieve_old_table_not_found():
    old_table = ReadmeUpdater.retrieve_old_table('./')

    assert old_table == ''


def test_read_current_readme():
    readme = ReadmeUpdater.read_current_readme('./mock-bad-dir')

    assert readme is None


def test_read_current_readme_does_not_exist():
    readme = ReadmeUpdater.read_current_readme('./')

    assert '# Homebrew Releaser' in readme


@mock.patch('homebrew_releaser.git.Git.add')
def test_replace_table_contents(mock_git_add):
    with mock.patch('builtins.open', mock.mock_open()):
        ReadmeUpdater.replace_table_contents(
            'mock file contents',
            'old table contents',
            'new table contents',
            './'
        )

    mock_git_add.assert_called_once()


def test_determine_readme():
    readme = ReadmeUpdater.determine_readme('./')

    assert readme == './README.md'