import logging
import os
import re
import subprocess

from pretty_tables import PrettyTables

from .constants import FORMULA_FOLDER, SUBPROCESS_TIMEOUT


def update_readme(homebrew_tap):
    """Updates the homebrew tap README by replacing the old table string
    with the updated table string
    """
    formulas = format_formula_data()
    new_table = generate_table(formulas)
    old_table = retrieve_old_table()
    readme_content = read_current_readme()
    replace_table_contents(readme_content, old_table, new_table, homebrew_tap)


def format_formula_data():
    """Retrieve the name, description, and homepage from each
    Ruby formula file in the homebrew tap repo
    """
    files = os.listdir('formula')
    formulas = []
    for filename in sorted(files):
        with open(f'{FORMULA_FOLDER}/{filename}', 'r') as formula:
            # TODO: Add error handling here when we retrieve bad info or no formula
            for i, line in enumerate(formula):
                if line.strip().startswith('class'):
                    name_line = line.split()
                    name_pieces = []
                    name_pieces = re.findall('[A-Z][^A-Z]*', name_line[1])
                    formatted_name = ''

                    for piece in name_pieces:
                        if piece != name_pieces[-1]:
                            formatted_name += f'{piece}-'
                        else:
                            formatted_name += f'{piece}'
                        final_name = formatted_name.lower()
                if line.strip().startswith('desc'):
                    final_desc = line.strip().replace('desc ', '').replace('"', '')
                if line.strip().startswith('homepage'):
                    final_homepage = line.strip().replace('homepage ', '').replace('"', '')
            formula_data = {
                'name': final_name,
                'desc': final_desc,
                'homepage': final_homepage,
            }
            formulas.append(formula_data)
    return formulas


def generate_table(formulas):
    """Generates a pretty table which will be used in the README file
    """
    headers = ['Project', 'Description', 'Installation']
    rows = []
    for formula in formulas:
        rows.append(
            [
                f'[{formula["name"]}]({formula.get("homepage")})',
                formula.get('desc'),
                f'`brew install {formula["name"]}`',
            ]
        )

    table = PrettyTables.generate_table(
        headers=headers,
        rows=rows,
        empty_cell_placeholder='NA',
    )

    return table


def retrieve_old_table():
    """Retrives all content between the start/end tags in the README file
    """
    with open('README.md', 'r') as readme:
        copy = False
        old_table = ''
        for line in readme:
            if line.strip() == '<!-- project_table_start -->':
                copy = True
                continue
            elif line.strip() == '<!-- project_table_end -->':
                copy = False
                continue
            elif copy:
                old_table += line

        # If we start copying but never find a closing tag or can't copy the old table content, raise an error
        if copy is True or old_table == '':
            # TODO: Do we want to exit here or simply log a warning?
            raise SystemExit('Could not find start/end tags for project table in README.')

        return old_table


def read_current_readme():
    """Reads the current README content
    """
    try:
        with open('README.md', 'r') as readme:
            file_content = readme.read()
            return file_content
        logging.debug(f'{readme} read successfully.')
    except Exception as error:
        raise SystemExit(error)


def replace_table_contents(file_content, old_table, new_table, homebrew_tap):
    """Replaces the old README project table string with the new
    project table string
    """
    try:
        with open('README.md', 'w') as readme:
            readme.write(file_content.replace(old_table, new_table + '\n'))
        logging.debug(f'{readme} written successfully.')
    except Exception as error:
        raise SystemExit(error)

    # TODO: Move this into its own function and rework how all git operations work
    try:
        output = subprocess.check_output(
            (
                f'cd {homebrew_tap}'
                f' && git add README.md'
            ),
            stdin=None,
            stderr=None,
            shell=True,
            timeout=SUBPROCESS_TIMEOUT
        )
        logging.debug('README added successfully.')
    except subprocess.TimeoutExpired as error:
        raise SystemExit(error)
    except subprocess.CalledProcessError as error:
        raise SystemExit(error)
    return output
