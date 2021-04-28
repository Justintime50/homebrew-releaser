# CHANGELOG

## v0.5.3 (2021-04-27)

* Properly navigate to git directory

## v0.5.2 (2021-04-27)

* Corrects Dockerfile copy command now that this is a package and not a single script

## v0.5.1 (2021-04-27)

* Fix bad import

## v0.5.0 (2021-04-27)

* Adds a feature to update the project table in the homebrew tap's README which includes all the formula name, descriptions, and installation commands (set `update_readme_table` to `true`)
* Drops the clone depth of a repo from `5` to `2`
* Changes the git config from a global scope to local scope (helps during testing by not accidentally blowing away real credentials)
* Various code refactor

## v0.4.3 (2021-02-01)

* Added automated releasing (retagging) of Homebrew Releaser via GitHub Actions. When a new version is released, GitHub Actions will automatically update the stable `v1` tag to point to the latest release

## v0.4.1 && v0.4.2 (2021-01-09)

* Small bug fix that sets the default formula folder

## v0.4.0 (2021-01-09)

* Overhauled the configurable options and provided more defaults out of the box. Changes include:
    * No longer support `owner` and `repo` as these variables are given to use by GitHub already
    * Changed `homebrew_formula_folder` to `formula_folder` - added a default of `formula`
    * Changed `owner_email` to `commit_email` and added `commit_owner` - added defaults of `homebrew-releaser@example.com` and `homebrew-releaser` respectively
    * Added `homebrew_owner` as an option to go alongside the already existing `homebrew_tap`, this allows you to release to a tap that may not be owned by the same person
* Updated documentation with all changes
* Cut out extra overhead on the Dockerfile to improve performance
* Properly format `desc` field to pass `brew audit` by stripping articles from the beginning if present and hard stops from the end (all periods and exclamations)
* Added additional logging for `info` and `debug` modes and fixed a typo in the output
* Added an optional env variable `skip_commit` which will skip committing the generated formula to a homebrew tap. Useful for local testing

## v0.3.0 (2021-01-06)

* Fixes `brew audit` lint rules by adding an extra line between magic comments and adding missing `typed: false` comment
* Added the `logging` module and replaced print statements
* 100% code coverage
* Code cleanup

## v0.2.1 & v0.2.2 && v0.2.3 (2021-01-05)

* Important bug fix required to get Homebrew Releaser running
* More unit tests

## v0.2.0 (2021-01-05)

* Changed name from `shell-releaser` to `homebrew-releaser` as this tool can really be used for any kind of script, binary, or executable
* Changed env variable of `bin_install` to simply `install` as you may not need/want to place your scripts in bin and use `system` instead
* Switch from `python-3.9` to `python3.9-alpine` Docker image for much faster performance. Manually install `git` and `perl-utils` in Docker image as we depend on them for correct operation
* Added try/except blocks and properly throw exit codes/messages for each functionality
* Added `test` input variable so you can specify tests
* Added checks and balances ensuring environment variables are set before running
* Added sane defaults for a few internal variables
* Added `license` to generated formula
* Maxing out git clone depth to the `latest 5 commits` to greatly improve performance on large homebrew taps
* Added unit tests
* Added GitHub Actions to lint and test the project
* Refactored code into smaller testable units, other various bug fixes

## v0.1.1 (2021-01-02)

* Adding missing args to `action.yml`
* Fixes Dockerfile to run in GitHub Actions environment
* Updated README with usage instructions
* Added a success message when the workflow completes

## v0.1.0 (2021-01-02)

* Initial release
* Generates a Homebrew formula file based off the latest release of a project updating the name, description, checksum, and tar url
