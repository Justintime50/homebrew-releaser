import os

from homebrew_releaser.formula import Formula

CASSETTE_PATH = 'test/cassettes'

USERNAME = 'Justintime50'
CHECKSUM = '0' * 64  # `brew audit` wants a 64 character number here, this would be true with real data
INSTALL = 'bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"'
DEPENDS_ON = """
"gcc"
"bash" => :build
"""
TEST = 'assert_match("my script output", shell_output("my-script-command"))'


def _record_cassette(cassette_path: str, cassette_name: str, cassette_data: str):
    """Read from existing file or create new file if it's not present (file = 'cassette').

    Tests using this function will generate a formula into a "cassette" file (similar to how
    vcrpy works for HTTP requests and responses: https://github.com/kevin1024/vcrpy) if it
    does not exist already.

    To regenerate the file (when changes are made to how formula are generated), simply
    delete the file (cassette for the associated test) and run tests again. Ensure that the
    output of the file is correct.
    """
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

    NOTE: See docstring in `_record_cassette` for more details on how recording cassettes works.
    """
    cassette_filename = 'test_formula_template.rb'
    mock_repo_name = cassette_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/v0.1.0.tar.gz'

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
        mock_repo_name,
        repository,
        CHECKSUM,
        INSTALL,
        mock_tar_url,
        DEPENDS_ON,
        TEST,
    )

    _record_cassette(CASSETTE_PATH, cassette_filename, formula)


def test_generate_formula_no_article_description():
    """Tests that we generate the formula content correctly (when there is no article
    that starts the description field).

    NOTE: See docstring in `_record_cassette` for more details on how recording cassettes works.
    """
    cassette_filename = 'test_formula_template_no_article_description.rb'
    mock_repo_name = cassette_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/v0.1.0.tar.gz'

    repository = {
        # Here we don't start the description off with an article
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': {'spdx_id': 'MIT'},
    }

    formula = Formula.generate_formula_data(
        USERNAME,
        mock_repo_name,
        repository,
        CHECKSUM,
        INSTALL,
        mock_tar_url,
        None,
        None,
    )

    _record_cassette(CASSETTE_PATH, cassette_filename, formula)


def test_generate_formula_no_depends_on():
    """Tests that we generate the formula content correctly (when no depends_on given).

    NOTE: See docstring in `_record_cassette` for more details on how recording cassettes works.
    """
    cassette_filename = 'test_formula_template_no_depends_on.rb'
    mock_repo_name = cassette_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/v0.1.0.tar.gz'

    repository = {
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': {'spdx_id': 'MIT'},
    }

    formula = Formula.generate_formula_data(
        USERNAME,
        mock_repo_name,
        repository,
        CHECKSUM,
        INSTALL,
        mock_tar_url,
        None,
        TEST,
    )

    _record_cassette(CASSETTE_PATH, cassette_filename, formula)


def test_generate_formula_no_test():
    """Tests that we generate the formula content correctly (when there is no test).

    NOTE: See docstring in `_record_cassette` for more details on how recording cassettes works.
    """
    cassette_filename = 'test_formula_template_no_test.rb'
    mock_repo_name = cassette_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/v0.1.0.tar.gz'

    repository = {
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': {'spdx_id': 'MIT'},
    }

    formula = Formula.generate_formula_data(
        USERNAME,
        mock_repo_name,
        repository,
        CHECKSUM,
        INSTALL,
        mock_tar_url,
        DEPENDS_ON,
        None,
    )

    _record_cassette(CASSETTE_PATH, cassette_filename, formula)
