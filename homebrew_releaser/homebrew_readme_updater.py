import os
import re

from pretty_tables import PrettyTables


def main():
    formulas = format_formula_data()
    new_table = generate_table(formulas)
    old_table = retrieve_old_table()
    readme_content = read_current_readme()
    replace_table_contents(readme_content, old_table, new_table)


def format_formula_data():
    files = os.listdir('formula')
    formulas = []
    for filename in sorted(files):
        with open('formula/' + filename, 'r') as formula:
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
    headers = ['Project', 'Description', 'Installation']
    rows = []
    for formula in formulas:
        rows.append(
            [f'[{formula["name"]}]({formula.get("homepage")})', formula.get(
                'desc'), f'`brew install {formula["name"]}`']
        )

    table = PrettyTables.generate_table(
        headers=headers,
        rows=rows,
        empty_cell_placeholder='NA',
    )

    return table


def retrieve_old_table():
    with open('README.md', 'r') as infile:
        copy = False
        old_table = ''
        for line in infile:
            if line.strip() == '<!-- project_table_start -->':
                copy = True
                continue
            elif line.strip() == '<!-- project_table_end -->':
                copy = False
                continue
            elif copy:
                old_table += line
        return old_table


def read_current_readme():
    with open('README.md', 'r') as infile:
        file_content = infile.read()
        return file_content


def replace_table_contents(file_content, old_table, new_table):
    with open('README.md', 'w') as outfile:
        outfile.write(file_content.replace(old_table, new_table + '\n'))


if __name__ == '__main__':
    main()
