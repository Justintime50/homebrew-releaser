# CHANGELOG

## v0.2.0 (TODO)

* Switch from `python-3.9` to `python3.9-alpine` Docker image for much faster performance. Manually install `git` and `perl-utils` in Docker image as we depend on them for correct operation

## v0.1.1 (2021-01-02)

* Adding missing args to `action.yml`
* Fixes Dockerfile to run in GitHub Actions environment
* Updated README with usage instructions
* Added a success message when the workflow completes

## v0.1.0 (2021-01-02)

* Initial release
* Generates a Homebrew formula file based off the latest release of a project updating the name, description, checksum, and tar url
