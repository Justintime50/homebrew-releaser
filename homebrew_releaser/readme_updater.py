import os
import re
from typing import List, Optional

import _io  # type: ignore
import pretty_tables
import woodchips

from homebrew_releaser.constants import FORMULA_FOLDER, LOGGER_NAME
from homebrew_releaser.git import Git


class ReadmeUpdater:
    @staticmethod
    def update_readme(homebrew_tap: str):
        """Updates the homebrew tap README by replacing the old table string
        with the updated table string.
        """
        formulas = ReadmeUpdater.format_formula_data(homebrew_tap)
        new_table = ReadmeUpdater.generate_table(formulas)
        old_table = ReadmeUpdater.retrieve_old_table(homebrew_tap)
        readme_content = ReadmeUpdater.read_current_readme(homebrew_tap)
        ReadmeUpdater.replace_table_contents(readme_content, old_table, new_table, homebrew_tap)

    @staticmethod
    def format_formula_data(homebrew_tap: str) -> List:
        """Retrieve the name, description, and homepage from each
        Ruby formula file in the homebrew tap repo.
        """
        homebrew_tap_path = os.path.join(homebrew_tap, FORMULA_FOLDER)
        formulas = []
        files = os.listdir(homebrew_tap_path)

        if len(files) == 0:
            raise SystemExit('No files found in the "formula_folder" provided.')

        try:
            for filename in sorted(files):
                with open(os.path.join(homebrew_tap_path, filename), 'r') as formula:
                    # Set empty defaults
                    final_name = ''
                    final_desc = ''
                    final_homepage = ''

                    for _, line in enumerate(formula):
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
        except Exception as error:
            raise SystemExit(f'There was a problem opening or reading the formula data: {error}')

        return formulas

    @staticmethod
    def generate_table(formulas: List) -> str:
        """Generates a pretty table which will be used in the README file."""
        headers = ['Project', 'Description', 'Install']
        rows = []

        for formula in formulas:
            rows.append(
                [
                    f'[{formula["name"]}]({formula.get("homepage")})',
                    formula.get('desc'),
                    f'`brew install {formula["name"]}`',
                ]
            )

        table = pretty_tables.create(
            headers=headers,
            rows=rows,
            empty_cell_placeholder='NA',
        )

        return table

    @staticmethod
    def retrieve_old_table(homebrew_tap: str) -> str:
        """Retrives all content between the start/end tags in the README file."""
        logger = woodchips.get(LOGGER_NAME)

        readme = ReadmeUpdater.determine_readme(homebrew_tap)
        old_table = ''

        if readme:
            with open(readme, 'r') as readme_contents:
                copy = False
                for line in readme_contents:
                    if line.strip() == '<!-- project_table_start -->':
                        copy = True
                        continue
                    elif line.strip() == '<!-- project_table_end -->':
                        copy = False
                        continue
                    elif copy:
                        old_table += line

                # If we start copying but never find a closing tag or can't copy the old table content, warn the user
                # NOTE: This will not fail the release workflow as this would be a bad experience for the user
                if copy is True or old_table == '':
                    logger.error('Could not find start/end tags for project table in README.')

        return old_table

    @staticmethod
    def read_current_readme(homebrew_tap: str) -> _io.TextIOWrapper:
        """Reads the current README content."""
        logger = woodchips.get(LOGGER_NAME)

        readme = ReadmeUpdater.determine_readme(homebrew_tap)
        file_content = None

        if readme:
            with open(readme, 'r') as readme_contents:
                file_content = readme_contents.read()
            logger.debug(f'{readme} read successfully.')

        return file_content

    @staticmethod
    def replace_table_contents(file_content: _io.TextIOWrapper, old_table: str, new_table: str, homebrew_tap: str):
        """Replaces the old README project table string with the new
        project table string.
        """
        logger = woodchips.get(LOGGER_NAME)

        readme = ReadmeUpdater.determine_readme(homebrew_tap)

        if readme:
            with open(readme, 'w') as readme_contents:
                readme_contents.write(file_content.replace(old_table, new_table + '\n'))
            logger.debug(f'{readme} written successfully.')

            Git.add(homebrew_tap)

    @staticmethod
    def determine_readme(homebrew_tap: str) -> Optional[str]:
        """Determines the README file to open. The README file must either be:

        1. completely uppercase or completely lowercase
        2. have the file extension of `.md`
        3. reside in the root of a project
        """
        logger = woodchips.get(LOGGER_NAME)

        readme_to_open = None
        uppercase_readme = os.path.join(homebrew_tap, 'README.md')
        lowercase_readme = os.path.join(homebrew_tap, 'readme.md')

        if os.path.isfile(uppercase_readme):
            readme_to_open = uppercase_readme
        elif os.path.isfile(lowercase_readme):
            readme_to_open = lowercase_readme
        else:
            logger.error('Could not find a valid README in this project to update.')

        return readme_to_open
