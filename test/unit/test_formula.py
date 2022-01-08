import os

from homebrew_releaser.formula import Formula

USERNAME = 'Justintime50'
REPO_NAME = 'homebrew-releaser'
CHECKSUM = '1234567890123456789012345678901234567890'
INSTALL = 'bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"'
TAR_URL = f'https://github.com/{USERNAME}/{REPO_NAME}/archive/v0.1.0.tar.gz'
DEPENDS_ON = """
"gcc"
"bash" => :build
"""
TEST = 'assert_match("my script output", shell_output("my-script-command"))'

CASSETTE_PATH = 'test/cassettes'


def _record_cassette(cassette_path: str, cassette_name: str, cassette_data: str):
    """Read from existing file or create new file if it's not present."""
    full_cassette_filename = os.path.join(cassette_path, cassette_name)

    if os.path.isfile(full_cassette_filename):
        with open(full_cassette_filename, 'r') as cassette_file:
            assert cassette_data == cassette_file.read()
    else:
        os.makedirs(cassette_path, exist_ok=True)
        with open(full_cassette_filename, 'w') as cassette_file:
            cassette_file.write(cassette_data)


def test_generate_formula():
    """Tests that we generate the formula content correctly when all parameters are passed.

    This test generates the formula "cassette" file if it does not exist already
    To regenerate the file (when changes are made to how formula are generated), simply
    delete the file and run tests again. Ensure the output of the file is correct.
    """
    repository = {
        # We use a badly written description string here on purpose to test our formatting code, this includes:
        # - starting with an article
        # - punctuation
        # - trailing whitespace
        # - extra capitilization
        'description': 'A tool to release... scripts, binaries, and executables to GitHub. ',
        'license': {'spdx_id': 'MIT'},
    }

    formula = Formula.generate_formula_data(
        USERNAME,
        REPO_NAME,
        repository,
        CHECKSUM,
        INSTALL,
        TAR_URL,
        DEPENDS_ON,
        TEST,
    )
    cassette_filename = 'test_formula_template.rb'

    _record_cassette(CASSETTE_PATH, cassette_filename, formula)


def test_generate_formula_no_article_description():
    """Tests that we generate the formula content correctly (when there is no article
    that starts the description field).

    This test generates the formula "cassette" file if it does not exist already
    To regenerate the file (when changes are made to how formula are generated), simply
    delete the file and run tests again. Ensure the output of the file is correct.
    """
    repository = {
        # Here we don't start the description off with an article
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': {'spdx_id': 'MIT'},
    }

    formula = Formula.generate_formula_data(USERNAME, REPO_NAME, repository, CHECKSUM, INSTALL, TAR_URL)
    cassette_filename = 'test_formula_template_no_article_description.rb'

    _record_cassette(CASSETTE_PATH, cassette_filename, formula)


def test_generate_formula_no_depends_on():
    """Tests that we generate the formula content correctly (when no depends_on given).

    This test generates the formula "cassette" file if it does not exist already
    To regenerate the file (when changes are made to how formula are generated), simply
    delete the file and run tests again. Ensure the output of the file is correct.
    """
    repository = {
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': {'spdx_id': 'MIT'},
    }

    formula = Formula.generate_formula_data(USERNAME, REPO_NAME, repository, CHECKSUM, INSTALL, TAR_URL, None, TEST)
    cassette_filename = 'test_formula_template_no_depends_on.rb'

    _record_cassette(CASSETTE_PATH, cassette_filename, formula)


def test_generate_formula_no_test():
    """Tests that we generate the formula content correctly (when there is no test).

    This test generates the formula "cassette" file if it does not exist already
    To regenerate the file (when changes are made to how formula are generated), simply
    delete the file and run tests again. Ensure the output of the file is correct.
    """
    repository = {
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': {'spdx_id': 'MIT'},
    }

    formula = Formula.generate_formula_data(USERNAME, REPO_NAME, repository, CHECKSUM, INSTALL, TAR_URL, DEPENDS_ON)
    cassette_filename = 'test_formula_template_no_test.rb'

    _record_cassette(CASSETTE_PATH, cassette_filename, formula)
