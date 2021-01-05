# CHANGELOG

## v0.2.1 (2021-01-05)

* Important bug fix and more tests

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
