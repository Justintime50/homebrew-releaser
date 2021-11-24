import re

import woodchips

from homebrew_releaser.constants import LOGGER_NAME


class Formula:
    @staticmethod
    def generate_formula_data(
        owner: str, repo_name: str, repository: str, checksum: str, install: str, tar_url: str, test: str
    ) -> str:
        """Generates the formula data for Homebrew.

        We attempt to ensure generated formula will pass `brew audit --strict --online` if given correct inputs:
        - Proper class name
        - 80 characters or less desc field (alphanumeric characters and does not start with an article)
        - Present homepage
        - URL points to the tar file
        - Checksum matches the url archive
        - Proper installable binary
        - Test is included
        - No version attribute if Homebrew can reliably infer the version from the tar URL (GitHub tag)
        """
        logger = woodchips.get(LOGGER_NAME)

        repo_name_length = len(repo_name)
        max_desc_field_length = 80
        max_desc_field_buffer = 2
        description_length = max_desc_field_length - repo_name_length + max_desc_field_buffer

        class_name = re.sub(r'[-_. ]+', '', repo_name.title())
        license_type = repository['license']['spdx_id']
        description = re.sub(r'[.!]+', '', repository['description'][:description_length]).strip().capitalize()

        # If the first word of the desc is an article, we cut it out per `brew audit`
        first_word_of_desc = description.split(' ', 1)
        if first_word_of_desc[0].lower() in ['a', 'an', 'the']:
            description = first_word_of_desc[1].strip().capitalize()

        # RUBY TEMPLATE DATA TO REMAIN DOUBLE SPACED
        test = (
            f"""
  test do
    {test.strip()}
  end
end"""
            if test
            else 'end'
        )

        template = f"""# typed: false
# frozen_string_literal: true

# This file was generated by Homebrew Releaser. DO NOT EDIT.
class {class_name} < Formula
  desc "{description}"
  homepage "https://github.com/{owner}/{repo_name}"
  url "{tar_url}"
  sha256 "{checksum}"
  license "{license_type}"

  def install
    {install.strip()}
  end
{test}
"""
        logger.debug('Homebrew formula generated successfully.')

        return template
