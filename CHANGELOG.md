# CHANGELOG

## NEXT RELEASE

- Generates a checksum for the auto-generate `.zip` release archive in addition the auto-generated `.tar.gz` archive

## v0.11.0 (2022-01-08)

- Added the `depends_on` key to formulas allowing users to specify dependencies for their formulas
- Reworked formula generation logic and tests to be more accurate and explicit for better formula generation (we now audit the test formula on CI)

## v0.10.0 (2021-12-12)

- Adds a `checksum.txt` file to the latest release of your repo containing the checksums of all "released" assets (binaries, scripts, etc)
- Bumps minimum version of Python from 3.7 to 3.9

## v0.9.2 (2021-12-07)

- Adds `mypy` type checking

## v0.9.1 (2021-11-24)

- Restores previous logger formatting for console output

## v0.9.0 (2021-11-24)

- Uses `woodchips` for logging
- Bumps `pretty_tables` to v2
- Bump Python version used from 3.9 to 3.10
- Adds Python type hinting

## v0.8.3 (2021-11-03)

- Fixes a bug that setup the git environment incorrectly after the shell refactor from the last release

## v0.8.2 (2021-11-02)

- Refactors shell operations to no longer invoke a shell when using the subprocess module. No longer change directories but instead call git operations directly from the destination path

## v0.8.1 (2021-10-25)

- Removes the `bottle :unneeded` from formula generation as it's been deprecated

## v0.8.0 (2021-09-10)

- Rebuild with the corrected `pretty-tables` library which re-adds the horizontal break between headers and row data
- Removes the `mock` library in favor of the builtin `unittest.mock` library
- Bumps the minimum Python version to 3.7

## v0.7.0 (2021-06-27)

- Refactored app completely by splitting up all logic into separate modules
- We now use the latest tag instead of release as releases can often be named instead of sticking to strict version numbers (closes #4, closes #7)
- Adds `an` to the list of articles to strip out of formula descriptions
- Changed `Installation` header in README updater to `Install`
- Added better error handling surrounding the README updater
- Exposed `DEBUG` logging to the user via the `debug: true` flag to assist in troubleshooting the GitHub Action if necessary
- Made all functions static methods
- Added better test coverage
- Split up git `add`, `commit`, and `push` functionality for better flexibilty
- Additional info and debugging statements for each step were added
- Various small improvements and bug fixes

## v0.6.0 (2021-05-31)

- Pins dependencies

## v0.5.6 (2021-04-27)

- I'm ashamed to need to release 7 versions in a single night...
- Bug fixes for opening/writing README file

## v0.5.5 (2021-04-27)

- Setup a testing environment via Docker to assist with end-to-end testing this github action locally
- Added more logging and renamed other output
- Variious bug fixes

## v0.5.4 (2021-04-27)

- Reworks git setup command order

## v0.5.3 (2021-04-27)

- Properly navigate to git directory

## v0.5.2 (2021-04-27)

- Corrects Dockerfile copy command now that this is a package and not a single script

## v0.5.1 (2021-04-27)

- Fix bad import

## v0.5.0 (2021-04-27)

- Adds a feature to update the project table in the homebrew tap's README which includes all the formula name, descriptions, and installation commands (set `update_readme_table` to `true`)
- Drops the clone depth of a repo from `5` to `2`
- Changes the git config from a global scope to local scope (helps during testing by not accidentally blowing away real credentials)
- Various code refactor

## v0.4.3 (2021-02-01)

- Added automated releasing (retagging) of Homebrew Releaser via GitHub Actions. When a new version is released, GitHub Actions will automatically update the stable `v1` tag to point to the latest release

## v0.4.1 && v0.4.2 (2021-01-09)

- Small bug fix that sets the default formula folder

## v0.4.0 (2021-01-09)

- Overhauled the configurable options and provided more defaults out of the box. Changes include:
  - No longer support `owner` and `repo` as these variables are given to use by GitHub already
  - Changed `homebrew_formula_folder` to `formula_folder` - added a default of `formula`
  - Changed `owner_email` to `commit_email` and added `commit_owner` - added defaults of `homebrew-releaser@example.com` and `homebrew-releaser` respectively
  - Added `homebrew_owner` as an option to go alongside the already existing `homebrew_tap`, this allows you to release to a tap that may not be owned by the same person
- Updated documentation with all changes
- Cut out extra overhead on the Dockerfile to improve performance
- Properly format `desc` field to pass `brew audit` by stripping articles from the beginning if present and hard stops from the end (all periods and exclamations)
- Added additional logging for `info` and `debug` modes and fixed a typo in the output
- Added an optional env variable `skip_commit` which will skip committing the generated formula to a homebrew tap. Useful for local testing

## v0.3.0 (2021-01-06)

- Fixes `brew audit` lint rules by adding an extra line between magic comments and adding missing `typed: false` comment
- Added the `logging` module and replaced print statements
- 100% code coverage
- Code cleanup

## v0.2.1 & v0.2.2 && v0.2.3 (2021-01-05)

- Important bug fix required to get Homebrew Releaser running
- More unit tests

## v0.2.0 (2021-01-05)

- Changed name from `shell-releaser` to `homebrew-releaser` as this tool can really be used for any kind of script, binary, or executable
- Changed env variable of `bin_install` to simply `install` as you may not need/want to place your scripts in bin and use `system` instead
- Switch from `python-3.9` to `python3.9-alpine` Docker image for much faster performance. Manually install `git` and `perl-utils` in Docker image as we depend on them for correct operation
- Added try/except blocks and properly throw exit codes/messages for each functionality
- Added `test` input variable so you can specify tests
- Added checks and balances ensuring environment variables are set before running
- Added sane defaults for a few internal variables
- Added `license` to generated formula
- Maxing out git clone depth to the `latest 5 commits` to greatly improve performance on large homebrew taps
- Added unit tests
- Added GitHub Actions to lint and test the project
- Refactored code into smaller testable units, other various bug fixes

## v0.1.1 (2021-01-02)

- Adding missing args to `action.yml`
- Fixes Dockerfile to run in GitHub Actions environment
- Updated README with usage instructions
- Added a success message when the workflow completes

## v0.1.0 (2021-01-02)

- Initial release
- Generates a Homebrew formula file based off the latest release of a project updating the name, description, checksum, and tar url
