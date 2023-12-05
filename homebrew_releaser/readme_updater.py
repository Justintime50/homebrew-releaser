import os
import re
from typing import (
    List,
    Optional,
    Tuple,
)

import _io  # type: ignore
import pretty_tables
import woodchips

from homebrew_releaser.constants import (
    FORMULA_FOLDER,
    LOGGER_NAME,
)


TABLE_START_TAG = '<!-- project_table_start -->'
TABLE_END_TAG = '<!-- project_table_end -->'


class ReadmeUpdater:
    @staticmethod
    def update_readme(homebrew_tap: str):
        """Updates the homebrew tap README by replacing the old table string
        with the updated table string if it can be found.
        """
        old_table, found_old_table = ReadmeUpdater.retrieve_old_table(homebrew_tap)

        # Only update the README table if both start/end tags were found
        if found_old_table:
            formulas = ReadmeUpdater.format_formula_data(homebrew_tap)
            new_table = ReadmeUpdater.generate_table(formulas)

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

        if not any([file.endswith('.rb') for file in files]):
            raise SystemExit('No Ruby files found in the "formula_folder" provided.')

        try:
            for filename in sorted(files):
                with open(os.path.join(homebrew_tap_path, filename), 'r') as formula:
                    # Set empty defaults
                    final_name = ''
                    final_desc = ''
                    final_homepage = ''

                    for line in formula:
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
        logger = woodchips.get(LOGGER_NAME)

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

        final_table = TABLE_START_TAG + '\n' + table + '\n' + TABLE_END_TAG + '\n'

        logger.debug(final_table)

        return final_table

    @staticmethod
    def retrieve_old_table(homebrew_tap: str) -> Tuple[str, bool]:
        """Retrives all content between the start/end tags in the README file."""
        logger = woodchips.get(LOGGER_NAME)

        readme = ReadmeUpdater.does_readme_exist(homebrew_tap)
        old_table_found = False
        table_start_found = False
        table_end_found = False
        old_table = ''

        if readme:
            with open(readme, 'r') as readme_contents:
                for line in readme_contents:
                    normalized_line = line.strip().lower()
                    if normalized_line == TABLE_START_TAG:
                        table_start_found = True
                    elif normalized_line == TABLE_END_TAG:
                        table_end_found = True

                    # Once we find the start tag, start building the potential replacement
                    if table_start_found:
                        old_table += line
                    # Once we find both start and end tags, break out of reading more README lines
                    if table_start_found and table_end_found:
                        old_table_found = True
                        break

            if old_table_found is False:
                # If we can't find both start/end tags, reset the table so we don't blow away unassociated README data
                old_table = ''
                logger.error('Could not find both start and end tags for project table in README.')
        else:
            logger.error('Could not find a valid README in this project to update.')

        return old_table, old_table_found

    @staticmethod
    def read_current_readme(homebrew_tap: str) -> _io.TextIOWrapper:
        """Reads the current README content."""
        logger = woodchips.get(LOGGER_NAME)

        readme = ReadmeUpdater.does_readme_exist(homebrew_tap)
        file_content = None

        if readme:
            with open(readme, 'r') as readme_contents:
                file_content = readme_contents.read()
            logger.debug(f'{readme} read successfully.')

        return file_content

    @staticmethod
    def replace_table_contents(file_content: _io.TextIOWrapper, old_table: str, new_table: str, homebrew_tap: str):
        """Replaces the old README project table string with the new
        project table string including start/end tags.
        """
        logger = woodchips.get(LOGGER_NAME)

        readme = ReadmeUpdater.does_readme_exist(homebrew_tap)

        if readme:
            with open(readme, 'w') as readme_contents:
                readme_contents.write(file_content.replace(old_table, new_table))
            logger.debug(f'{readme} table updated successfully.')

    @staticmethod
    def does_readme_exist(homebrew_tap: str) -> Optional[str]:
        """Determines the README file to open. The README file must either:

        1. Have the file extension of `.md`
        2. Reside in the root of a project
        """
        readme_to_open = None
        readme_filename = 'readme.md'
        files = os.listdir(homebrew_tap)

        for filename in files:
            if filename.lower() == readme_filename:
                readme_to_open = os.path.join(homebrew_tap, filename)
                break

        return readme_to_open
