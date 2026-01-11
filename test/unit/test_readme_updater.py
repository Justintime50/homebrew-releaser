from unittest.mock import (
    mock_open,
    patch,
)

import pytest

from homebrew_releaser.readme_updater import (
    _does_readme_exist,
    _format_formula_data,
    _generate_table,
    _read_current_readme,
    _replace_table_contents,
    _retrieve_old_table,
    update_readme,
)


@patch("homebrew_releaser.readme_updater._format_formula_data")
@patch("homebrew_releaser.readme_updater._generate_table")
@patch("homebrew_releaser.readme_updater._retrieve_old_table", return_value=["", True])
@patch("homebrew_releaser.readme_updater._read_current_readme")
@patch("homebrew_releaser.readme_updater._replace_table_contents")
def test_update_readme(
    mock_replace_table_contents,
    mock_read_current_readme,
    mock_retrieve_old_table,
    mock_generate_table,
    mock_format_formula_data,
):
    """Tests that we update the README table when we can find the old table correctly."""
    update_readme("./")

    mock_format_formula_data.assert_called_once()
    mock_generate_table.assert_called_once()
    mock_retrieve_old_table.assert_called_once()
    mock_read_current_readme.assert_called_once()
    mock_replace_table_contents.assert_called_once()


@patch("homebrew_releaser.readme_updater._format_formula_data")
@patch("homebrew_releaser.readme_updater._generate_table")
@patch("homebrew_releaser.readme_updater._retrieve_old_table", return_value=["", False])
@patch("homebrew_releaser.readme_updater._read_current_readme")
@patch("homebrew_releaser.readme_updater._replace_table_contents")
def test_update_readme_cannot_find_old_table(
    mock_replace_table_contents,
    mock_read_current_readme,
    mock_retrieve_old_table,
    mock_generate_table,
    mock_format_formula_data,
):
    """Tests that when we cannot retrieve the old table that we skip updating with new details."""
    update_readme("./")

    # We should try to get the old table
    mock_retrieve_old_table.assert_called_once()

    # We should fail at doing anything with the new table
    mock_format_formula_data.assert_not_called()
    mock_generate_table.assert_not_called()
    mock_read_current_readme.assert_not_called()
    mock_replace_table_contents.assert_not_called()


@patch("homebrew_releaser.utils.WORKING_DIR", "")
@patch("homebrew_releaser.readme_updater.FORMULA_FOLDER", "test/unit")
def test_format_formula_data_no_ruby_files():
    """Tests that we throw an error when the formula folder provided does not contain any
    Ruby files (formula files).
    """
    with pytest.raises(SystemExit) as error:
        _format_formula_data("./")

    assert str(error.value) == 'No Ruby files found in the "formula_folder" provided.'


@patch("homebrew_releaser.utils.WORKING_DIR", "")
@patch("homebrew_releaser.readme_updater.FORMULA_FOLDER", "formulas")
def test_format_formula_data():
    """Tests that we build a list of formula metadata correctly based on what we found in the repo.

    Here, we reuse our 'recorded' formulas from the test suite as the dummy formulas that may have
    been found in a user's git repo.
    """
    formulas = _format_formula_data("test")

    assert len(formulas) == 17
    assert formulas[1] == {
        "name": "test-generate-formula",
        "desc": "Tool to release... scripts, binaries, & executables to github",
        "homepage": "https://github.com/Justintime50/test-generate-formula",
    }


@patch("homebrew_releaser.utils.WORKING_DIR", "")
@patch("homebrew_releaser.readme_updater.FORMULA_FOLDER", "formulas")
def test_format_formula_data_error_reading_formula():
    """Tests that we throw an error when we cannot properly read formula data."""
    with patch("builtins.open", mock_open()) as mock_opening:
        mock_opening.side_effect = OSError
        with pytest.raises(SystemExit) as error:
            _format_formula_data("test")

    assert str(error.value) == "There was a problem opening or reading the formula data: "


def test_generate_table():
    """Tests that we can properly generate the README table content"""
    formulas = [
        {
            "name": "mock-formula",
            "homepage": "https://github.com/justintime50/mock-formula",
            "desc": "mock description",
        },
    ]
    table = _generate_table(formulas)

    # fmt: off
    assert table == (
        '<!-- project_table_start -->\n'
        '| Project                                                      | Description      | Install                     |\n' # noqa
        '| ------------------------------------------------------------ | ---------------- | --------------------------- |\n' # noqa
        '| [mock-formula](https://github.com/justintime50/mock-formula) | mock description | `brew install mock-formula` |\n' # noqa
        '<!-- project_table_end -->\n'
    )
    # fmt: on


@patch("homebrew_releaser.utils.WORKING_DIR", "")
def test_retrieve_old_table_not_found():
    """Tests that we set the `table_found` variable to False when we can't find opening/closing README tags."""
    old_table, old_table_found = _retrieve_old_table("./")

    assert old_table == ""
    assert old_table_found is False


@patch("homebrew_releaser.utils.WORKING_DIR", "")
@pytest.mark.parametrize(
    "table_content",
    [
        """<!-- project_table_start -->
here is some mock data...
<!-- project_table_end -->""",
        """<!-- project_table_start -->
<!-- project_table_end -->""",
        """<!-- project_table_start -->

<!-- project_table_end -->""",
    ],
)
def test_retrieve_old_table(table_content):
    """Tests that we retrieve only the old table data when start and end tags exist.

    We ensure that regardless of table content (null, filled, or newline) that this works."""
    with patch("builtins.open", mock_open(read_data=table_content)):
        old_table, old_table_found = _retrieve_old_table("./")

    assert old_table == table_content
    assert old_table_found is True


@patch("homebrew_releaser.utils.WORKING_DIR", "")
@patch("logging.Logger.error")
def test_retrieve_old_table_no_readme(mock_logger):
    """Tests that we retrieve only the old table data when start and end tags exist."""
    old_table, old_table_found = _retrieve_old_table("test")

    mock_logger.assert_called_once_with("Could not find a valid README in this project to update.")
    assert old_table == ""
    assert old_table_found is False


@patch("homebrew_releaser.utils.WORKING_DIR", "")
def test_read_current_readme_does_not_exist():
    """Tests that the file contents of a README that doesn't exist is empty."""
    readme = _read_current_readme("test")

    assert readme == ""


@patch("homebrew_releaser.utils.WORKING_DIR", "")
def test_read_current_readme():
    """Tests that the content of a README found is returned."""
    readme = _read_current_readme("./")

    assert "# Homebrew Releaser" in readme


@patch("homebrew_releaser.utils.WORKING_DIR", "")
def test_replace_table_contents():
    """Test that we add the new README changes to git."""
    with patch("builtins.open", mock_open()):
        _replace_table_contents(
            file_content="mock file contents",
            old_table="old table contents",
            new_table="new table contents",
            homebrew_tap="./",
        )


@patch("homebrew_releaser.utils.WORKING_DIR", "")
@patch("logging.Logger.debug")
@patch("homebrew_releaser.app.add_git")
def test_replace_table_contents_no_readme(mock_git_add, mock_logger):
    """Tests that we do not run through the update readme block when there is no readme."""
    _replace_table_contents(
        file_content="mock file contents",
        old_table="old table contents",
        new_table="new table contents",
        homebrew_tap="test",
    )

    mock_logger.assert_not_called()


@patch("homebrew_releaser.utils.WORKING_DIR", "")
def test_does_readme_exist():
    """Tests that we can find a README in a directory."""
    readme = _does_readme_exist("./")

    assert readme == "./README.md"
