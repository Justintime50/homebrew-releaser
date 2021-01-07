<div align="center">

# Homebrew Releaser

Release scripts, binaries, and executables directly to Homebrew via GitHub Actions.

[![Build](https://github.com/Justintime50/homebrew-releaser/workflows/build/badge.svg)](https://github.com/Justintime50/homebrew-releaser/actions)
[![Coverage Status](https://coveralls.io/repos/github/Justintime50/homebrew-releaser/badge.svg?branch=main)](https://coveralls.io/github/Justintime50/homebrew-releaser?branch=main)
[![Licence](https://img.shields.io/github/license/Justintime50/homebrew-releaser)](LICENSE)

<img src="assets/showcase.png" alt="Showcase">

</div>

Homebrew Releaser allows you to release scripts, binaries, and executables directly to a personal Homebrew tap via a GitHub Action. I love what the team at [GoReleaser](https://github.com/goreleaser/goreleaser) did and wanted to replicate that on a smaller scale for simple items like shell scripts or other binaries I wanted to distribute. 

## Usage

Cut a new release on your GitHub project and let Homebrew Releaser publish that release via your personal Homebrew tap. Homebrew Releaser will update the project description, version, tar archive url, license, checksum, and any other required info so you don't have to.

**Note:** Shell scripts distributed via Homebrew Releaser must be executable and contain a proper shebang to work.
**Note:** Homebrew Releaser will always use the latest release of a GitHub project.

### GitHub Actions YML

Add the following to your `.github/workflows/release.yml` file in your GitHub repo. Alter the below records as needed.

```yml
on:
  push:
    tags:
      - "*"

jobs:
  homebrew-releaser:
    runs-on: ubuntu-latest
    name: homebrew-releaser
    steps:
      - name: Release my project to my Homebrew tap
        uses: Justintime50/homebrew-releaser@v0.3.0
        with:
          owner: Justintime50
          owner_email: justin@example.com
          repo: my_repo_name
          install: 'bin.install "src/my-script.sh" => "my-script"'
          test: 'assert_match("my script output", shell_output("my-script-command"))'
          homebrew_tap: homebrew-formulas
          homebrew_formula_folder: formula
          github_token: ${{ secrets.MY_GITHUB_TOKEN }}
```

**Options**

* `owner`: GitHub owner (username)
* `owner_email`: Email of the GitHub user (for commit config, if you'd rather not specify an email, `homebrew-releaser@example.com` will be used)
* `repo`: Name of the repository as it appears on GitHub
* `install`: The Homebrew command to copy your script to `bin`
* `test`: The Homebrew command to test your formula (optional field, if no test input is provided, no test block will be generated)
* `homebrew_tap`: The name of the homebrew tap as it appears on GitHub
* `homebrew_formula_folder`: The directory where your formula reside in your tap repo
* `github_token`: The GitHub Token secret that has `repo` permissions to the repo you want to release to

### Run manually

```bash
# The following environment variables must be set
INPUT_GITHUB_TOKEN=123...
INPUT_OWNER=Justintime50
INPUT_OWNER_EMAIL=justin@example.com
INPUT_REPO=my_repo_name
INPUT_INSTALL="bin.install \"src/my-script.sh\" => \"my-script\""
INPUT_TEST="assert_match(\"my script output\", shell_output(\"my-script\"))"
INPUT_HOMEBREW_TAP=homebrew-formulas
INPUT_HOMEBREW_FORMULA_FOLDER=formula

# Run from Docker, do not run on bare metal (it will replace your git config)
docker-compose up -d --build
```

## Development

```bash
# Install locally
make install

# Lint the project
make lint

# Run tests
make test

# Run test coverage
make coverage

# Get Makefile help
make help
```

## Attribution

* Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
