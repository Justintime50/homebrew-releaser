import os

from homebrew_releaser.formula import Formula

formula_path = 'test/formulas'

USERNAME = 'Justintime50'
VERSION = '0.1.0'
CHECKSUM = '0' * 64  # `brew audit` wants a 64 character number here, this would be true with real data
INSTALL = 'bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"'
# Dependencies are purposefully out of order so we can test that they get ordered properly for `brew audit`
DEPENDS_ON = """
"gcc"
"bash" => :build
"""
TEST = 'assert_match("my script output", shell_output("my-script-command"))'


def _record_formula(formula_path: str, formula_name: str, formula_data: str):
    """Read from existing formula file or create new formula file if it's not present.

    Tests using this function will generate a formula into a file (similar to how
    `vcrpy` works for HTTP requests and responses: https://github.com/kevin1024/vcrpy) if it
    does not exist already.

    To regenerate the file (when changes are made to how formula are generated), simply
    delete the file and run tests again. Ensure that the output of the file is correct.
    """
    full_cassette_filename = os.path.join(formula_path, formula_name)

    if os.path.isfile(full_cassette_filename):
        with open(full_cassette_filename, 'r') as cassette_file:
            assert formula_data == cassette_file.read()
    else:
        os.makedirs(formula_path, exist_ok=True)
        with open(full_cassette_filename, 'w') as cassette_file:
            cassette_file.write(formula_data)


def test_generate_formula():
    """Tests that we generate the formula content correctly when all parameters are passed
    (except a matrix so that we can test the auto-generate URL/checksum from GitHub).

    NOTE: See docstring in `_record_formula` for more details on how recording cassettes works.
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
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                f'{mock_repo_name}.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
                },
            }
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=DEPENDS_ON,
        test=TEST,
        matrix=None,
    )

    _record_formula(formula_path, cassette_filename, formula)


def test_generate_formula_no_article_description():
    """Tests that we generate the formula content correctly (when there is no article
    that starts the description field).

    NOTE: See docstring in `_record_formula` for more details on how recording cassettes works.
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
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                f'{mock_repo_name}.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
                },
            }
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=None,
        matrix=None,
    )

    _record_formula(formula_path, cassette_filename, formula)


def test_generate_formula_no_depends_on():
    """Tests that we generate the formula content correctly (when no depends_on given).

    NOTE: See docstring in `_record_formula` for more details on how recording cassettes works.
    """
    cassette_filename = 'test_formula_template_no_depends_on.rb'
    mock_repo_name = cassette_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/v0.1.0.tar.gz'

    repository = {
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': {'spdx_id': 'MIT'},
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                f'{mock_repo_name}.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
                },
            }
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=TEST,
        matrix=None,
    )

    _record_formula(formula_path, cassette_filename, formula)


def test_generate_formula_no_test():
    """Tests that we generate the formula content correctly (when there is no test).

    NOTE: See docstring in `_record_formula` for more details on how recording cassettes works.
    """
    cassette_filename = 'test_formula_template_no_test.rb'
    mock_repo_name = cassette_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/v0.1.0.tar.gz'

    repository = {
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': {'spdx_id': 'MIT'},
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                f'{mock_repo_name}.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': f'https://github.com/justintime50/{mock_repo_name}/releases/download/{VERSION}/{mock_repo_name}-{VERSION}.tar.gz',  # noqa
                },
            }
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=DEPENDS_ON,
        test=None,
        matrix=None,
    )

    _record_formula(formula_path, cassette_filename, formula)


def test_generate_formula_complete_matrix():
    """Tests that we generate the formula content correctly when we provide a complete OS matrix.

    NOTE: See docstring in `_record_formula` for more details on how recording cassettes works.
    """
    cassette_filename = 'test_formula_template_complete_matrix.rb'
    mock_repo_name = cassette_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/v0.1.0.tar.gz'

    repository = {
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': {'spdx_id': 'MIT'},
    }

    matrix = {
        'darwin': {
            'amd64': True,
            'arm64': True,
        },
        'linux': {
            'amd64': True,
            'arm64': True,
        },
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                'test-formula-template-complete-matrix.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-template-complete-matrix',  # noqa
                },
            },
            {
                'test-formula-0.1.0-darwin-amd64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-amd64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-darwin-arm64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-arm64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-linux-amd64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-amd64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-linux-arm64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-arm64.tar.gz',  # noqa
                },
            },
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=DEPENDS_ON,
        test=TEST,
        matrix=matrix,
    )

    _record_formula(formula_path, cassette_filename, formula)


def test_generate_formula_darwin_matrix():
    """Tests that we generate the formula content correctly when we provide a Darwin matrix.

    NOTE: See docstring in `_record_formula` for more details on how recording cassettes works.
    """
    cassette_filename = 'test_formula_template_darwin_matrix.rb'
    mock_repo_name = cassette_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/v0.1.0.tar.gz'

    repository = {
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': {'spdx_id': 'MIT'},
    }

    matrix = {
        'darwin': {
            'amd64': True,
            'arm64': True,
        },
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                'test-formula-template-darwin-matrix.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-template-darwin-matrix.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-darwin-amd64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-amd64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-darwin-arm64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-darwin-arm64.tar.gz',  # noqa
                },
            },
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=None,
        matrix=matrix,
    )

    _record_formula(formula_path, cassette_filename, formula)


def test_generate_formula_linux_matrix():
    """Tests that we generate the formula content correctly when we provide a Linux matrix.

    NOTE: See docstring in `_record_formula` for more details on how recording cassettes works.
    """
    cassette_filename = 'test_formula_template_linux_matrix.rb'
    mock_repo_name = cassette_filename.replace('_', '-').replace('.rb', '')
    mock_tar_url = f'https://github.com/{USERNAME}/{mock_repo_name}/archive/v0.1.0.tar.gz'

    repository = {
        'description': 'Release scripts, binaries, and executables to GitHub',
        'license': {'spdx_id': 'MIT'},
    }

    matrix = {
        'linux': {
            'amd64': True,
            'arm64': True,
        },
    }

    formula = Formula.generate_formula_data(
        owner=USERNAME,
        repo_name=mock_repo_name,
        repository=repository,
        checksums=[
            {
                'test-formula-template-linux-matrix.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-template-linux-matrix.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-linux-amd64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-amd64.tar.gz',  # noqa
                },
            },
            {
                'test-formula-0.1.0-linux-arm64.tar.gz': {
                    'checksum': CHECKSUM,
                    'url': 'https://github.com/justintime50/test-formula/releases/download/0.1.0/test-formula-0.1.0-linux-arm64.tar.gz',  # noqa
                },
            },
        ],
        install=INSTALL,
        tar_url=mock_tar_url,
        depends_on=None,
        test=None,
        matrix=matrix,
    )

    _record_formula(formula_path, cassette_filename, formula)
