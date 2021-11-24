import os

from homebrew_releaser.formula import Formula


def _record_cassette(cassette_path: str, cassette_name: str, cassette_data: str):
    """Read from existing file or create new file if it's not present"""
    full_cassette_filename = os.path.join(cassette_path, cassette_name)

    if os.path.isfile(full_cassette_filename):
        with open(full_cassette_filename, 'r') as cassette_file:
            assert cassette_data == cassette_file.read()
    else:
        os.makedirs(cassette_path, exist_ok=True)
        with open(full_cassette_filename, 'w') as cassette_file:
            cassette_file.write(cassette_data)


def test_generate_formula():
    """This test generates the formula "cassette" file if it does not exist already
    To regenerate the file (when changes are made to how formula are generated), simply
    delete the file and run tests again. Ensure the output of the file is correct.
    """
    username = 'Justintime50'
    repo_name = 'homebrew-releaser'
    repository = {
        # We use a badly written description string here on purpose to test our formatting code
        'description': 'A tool to release... scripts, binaries, and executables to GitHub. ',
        'license': {'spdx_id': 'MIT'},
    }
    checksum = '1234567890123456789012345678901234567890'
    install = 'bin.install "src/secure-browser-kiosk.sh" => "secure-browser-kiosk"'
    tar_url = f'https://github.com/{username}/{repo_name}/archive/v0.1.0.tar.gz'
    test = 'assert_match("my script output", shell_output("my-script-command"))'

    formula = Formula.generate_formula_data(username, repo_name, repository, checksum, install, tar_url, test)
    cassette_filename = 'test_formula_template.rb'
    cassette_path = 'test/cassettes'

    _record_cassette(cassette_path, cassette_filename, formula)
