<div align="center">

# Shell Releaser

Release shell scripts directly via Homebrew.

[![Build](https://github.com/Justintime50/shell-releaser/workflows/build/badge.svg)](https://github.com/Justintime50/shell-releaser/actions)
[![Coverage Status](https://coveralls.io/repos/github/Justintime50/shell-releaser/badge.svg?branch=main)](https://coveralls.io/github/Justintime50/shell-releaser?branch=main)
[![Licence](https://img.shields.io/github/license/Justintime50/shell-releaser)](LICENSE)

<img src="assets/showcase.png" alt="Showcase">

</div>

**Note:** This project is still in development. Star the project and keep an eye on the releases.

This project was inspired by [GoReleaser](https://github.com/goreleaser/goreleaser) which allows you to deliver Go binaries quickly via Homebrew. I wanted to do the same for shell scripts but couldn't immediately find a solution - so I decided to build one. Shell Releaser allows you to release shell scripts directly to Homebrew via a GitHub Action. Cut a new release on your favorite shell script project and let Shell Releaser publish that release via your self-hosted Homebrew tap. Shell Releaser will update the project description, version, tar archive url, and checksum for you.

## Install

To use in your project, see `Usage` below.

```bash
# Install locally
make install

# Get Makefile help
make help
```

## Usage

**Note:** Do not edit auto-generated formula files, it could lead to failures during operation.

Shell Releaser will always use the latest release of a GitHub project.

```bash
# Run manually
INPUT_GITHUB_TOKEN=123... OWNER=Justintime50 OWNER_EMAIL=justin@example.com REPO=freedom BIN_INSTALL='"src/secure-browser-kiosk.sh" => "secure-browser-kiosk"' HOMEBREW_TAP=homebrew-formulas HOMEBREW_FORMULA_FOLDER=formula venv/bin/python shell_releaser/releaser.py
```

Add the following to your `.github/workflows/release.yml` file in your GitHub repo. Alter the below records as needed.

* owner: GitHub username
* owner_email: Email of the GitHub user (for commit config)
* repo: Name of the repository as it appears on GitHub
* bin_install: The Homebrew command to copy your script to `bin`
* homebrew_tap: The name of the homebrew tap as it appears on GitHub
* homebrew_formula_folder: The directory where your formula reside in your tap repo
* github_token: The GitHub Token secret that has `repo` permissions to the repo you want to release to.

```yml
on:
  push:
    tags:
      - '*'

jobs:
  shell-releaser:
    runs-on: ubuntu-latest
    name: Release my shell script to Homebrew
    steps:
    - name: Release my shell script to Homebrew
      uses: Justintime50/shell-releaser@v0.1.1
      with:
        owner: Justintime50
        owner_email: justin@example.com
        repo: my_repo_name
        bin_install: '"src/my-script.sh" => "my-script"'
        homebrew_tap: 'homebrew-formulas'
        homebrew_formula_folder: formula
        github_token: ${{ secrets.MY_GITHUB_TOKEN }}
```

## Development

```bash
# Lint the project
make lint

# Run tests
make test

# Run test coverage
make coverage
```

## Attribution

* Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
