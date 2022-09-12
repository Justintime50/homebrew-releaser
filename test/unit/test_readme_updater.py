from unittest.mock import mock_open, patch

import pytest

from homebrew_releaser.readme_updater import ReadmeUpdater


@patch('homebrew_releaser.readme_updater.ReadmeUpdater.format_formula_data')
@patch('homebrew_releaser.readme_updater.ReadmeUpdater.generate_table')
@patch('homebrew_releaser.readme_updater.ReadmeUpdater.retrieve_old_table', return_value=['', True])
@patch('homebrew_releaser.readme_updater.ReadmeUpdater.read_current_readme')
@patch('homebrew_releaser.readme_updater.ReadmeUpdater.replace_table_contents')
def test_update_readme(
    mock_replace_table_contents,
    mock_read_current_readme,
    mock_retrieve_old_table,
    mock_generate_table,
    mock_format_formula_data,
):
    """Tests that we update the README table when we can find the old table correctly."""
    ReadmeUpdater.update_readme('./')

    mock_format_formula_data.assert_called_once()
    mock_generate_table.assert_called_once()
    mock_retrieve_old_table.assert_called_once()
    mock_read_current_readme.assert_called_once()
    mock_replace_table_contents.assert_called_once()


@patch('homebrew_releaser.readme_updater.ReadmeUpdater.format_formula_data')
@patch('homebrew_releaser.readme_updater.ReadmeUpdater.generate_table')
@patch('homebrew_releaser.readme_updater.ReadmeUpdater.retrieve_old_table', return_value=['', False])
@patch('homebrew_releaser.readme_updater.ReadmeUpdater.read_current_readme')
@patch('homebrew_releaser.readme_updater.ReadmeUpdater.replace_table_contents')
def test_update_readme_cannot_find_old_table(
    mock_replace_table_contents,
    mock_read_current_readme,
    mock_retrieve_old_table,
    mock_generate_table,
    mock_format_formula_data,
):
    """Tests that when we cannot retrieve the old table that we skip updating with new details."""
    ReadmeUpdater.update_readme('./')

    # We should try to get the old table
    mock_retrieve_old_table.assert_called_once()

    # We should fail at doing anything with the new table
    mock_format_formula_data.assert_not_called()
    mock_generate_table.assert_not_called()
    mock_read_current_readme.assert_not_called()
    mock_replace_table_contents.assert_not_called()


# TODO: Add a test that formats the data, this is difficult because we need a mock git repo
def test_format_formula_data_not_found():
    with pytest.raises(FileNotFoundError):
        ReadmeUpdater.format_formula_data('./')


def test_generate_table():
    formulas = [
        {
            'name': 'mock-formula',
            'homepage': 'https://github.com/justintime50/mock-formula',
            'desc': 'mock description',
        },
    ]
    table = ReadmeUpdater.generate_table(formulas)

    # fmt: off
    assert table == (
        '| Project                                                      | Description      | Install                     |\n' # noqa
        '| ------------------------------------------------------------ | ---------------- | --------------------------- |\n' # noqa
        '| [mock-formula](https://github.com/justintime50/mock-formula) | mock description | `brew install mock-formula` |' # noqa
    )
    # fmt: on


# TODO: Add another test with a table in the README
def test_retrieve_old_table_not_found():
    old_table, old_table_found = ReadmeUpdater.retrieve_old_table('./')

    assert old_table == ''
    assert old_table_found is False


def test_read_current_readme():
    readme = ReadmeUpdater.read_current_readme('./mock-bad-dir')

    assert readme is None


def test_read_current_readme_does_not_exist():
    readme = ReadmeUpdater.read_current_readme('./')

    assert '# Homebrew Releaser' in readme


@patch('homebrew_releaser.git.Git.add')
def test_replace_table_contents(mock_git_add):
    with patch('builtins.open', mock_open()):
        ReadmeUpdater.replace_table_contents('mock file contents', 'old table contents', 'new table contents', './')

    mock_git_add.assert_called_once()


def test_determine_readme():
    readme = ReadmeUpdater.determine_readme('./')

    assert readme == './README.md'
