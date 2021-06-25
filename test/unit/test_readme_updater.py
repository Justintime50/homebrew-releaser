import mock
import pytest
from homebrew_releaser.readme_updater import ReadmeUpdater


def test_read_current_readme():
    readme = ReadmeUpdater.read_current_readme('./mock-bad-dir')

    assert readme is None


def test_read_current_readme_does_not_exist():
    readme = ReadmeUpdater.read_current_readme('./')

    assert '# Homebrew Releaser' in readme


def test_replace_table_contents():
    pass


def test_determine_readme():
    readme = ReadmeUpdater.determine_readme('./')

    assert readme == './README.md'
