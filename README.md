<div align="center">

# Homebrew Releaser

Release scripts, binaries, and executables directly to Homebrew via GitHub Actions.

[![Build](https://github.com/Justintime50/homebrew-releaser/workflows/build/badge.svg)](https://github.com/Justintime50/homebrew-releaser/actions)
[![Coverage Status](https://coveralls.io/repos/github/Justintime50/homebrew-releaser/badge.svg?branch=main)](https://coveralls.io/github/Justintime50/homebrew-releaser?branch=main)
[![Version](https://img.shields.io/github/v/tag/justintime50/homebrew-releaser)](https://github.com/justintime50/homebrew-releaser/releases)
[![Licence](https://img.shields.io/github/license/Justintime50/homebrew-releaser)](LICENSE)

<img src="assets/showcase.png" alt="Showcase">

</div>

Homebrew Releaser allows you to release scripts, binaries, and executables directly to a personal Homebrew tap via a GitHub Action. I love what the team at [GoReleaser](https://github.com/goreleaser/goreleaser) did and wanted to replicate that on a smaller scale for simple items like shell scripts or other binaries I wanted to distribute. 

## Usage

**Notes:** 
* Shell scripts distributed via Homebrew Releaser must be executable and contain a proper shebang to work.
* Homebrew Releaser will always use the latest tag of a GitHub project. Git tags must follow semantic versioning for Homebrew to properly infer the installation instructions (eg: `v1.2.0` or 0.3.0`, etc).
* The Homebrew formula filename will match the github repo name.

### GitHub Actions YML

After releasing to GitHub, Homebrew Releaser can publish that release to a personal Homebrew tap by updating the project description, version, tar archive url, license, checksum, installation and testing command, and any other required info so you don't have to. You can check the [Homebrew documentation](https://docs.brew.sh/) and the [formula cookbook](https://docs.brew.sh/Formula-Cookbook) for more details on setting up a Homebrew formula or tap.

```yml
# .github/workflows/release.yml
# Start Homebrew Releaser when a new tag is created
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
        uses: Justintime50/homebrew-releaser@v1
        with:
          # The name of the homebrew tap to publish your formula to as it appears on GitHub.
          # Required.
          homebrew_owner: Justintime50
          homebrew_tap: homebrew-formulas

          # The name of the folder in your homebrew tap where formula will be committed to.
          # Default is shown.
          formula_folder: formula

          # The GitHub Token (saved as a repo secret) that has `repo` permissions for the homebrew tap you want to release to.
          # Required.
          github_token: ${{ secrets.HOMEBREW_TAP_GITHUB_TOKEN }}

          # Git author info used to commit to the homebrew tap.
          # Defaults are shown.
          commit_owner: homebrew-releaser
          commit_email: homebrew-releaser@example.com

          # Custom install command for your formula.
          # Required.
          install: 'bin.install "src/my-script.sh" => "my-script"'

          # Custom test command for your formula so you can run `brew test`.
          # Optional.
          test: 'assert_match("my script output", shell_output("my-script-command"))'

          # Skips committing the generated formula to a homebrew tap (useful for local testing).
          # Default is shown.
          skip_commit: false

          # Update your homebrew tap's README with a table of all projects in the tap.
          # This is done by pulling the information from all your formula.rb files - eg:
          #
          # | Project                                    | Description  | Install                  |
          # | ------------------------------------------ | ------------ | ------------------------ |
          # | [formula_1](https://github.com/user/repo1) | helpful text | `brew install formula_1` |
          # | [formula_1](https://github.com/user/repo2) | helpful text | `brew install formula_2` |
          # | [formula_1](https://github.com/user/repo3) | helpful text | `brew install formula_3` |
          #
          # Simply place the following in your README or wrap your project in these comment tags:
          # <!-- project_table_start -->
          # TABLE HERE
          # <!--project_table_end -->
          #
          # Finally, mark `update_readme_table` as `true` in your GitHub Action config and we'll do the work of building a custom table for you.
          # Default is `false`.
          update_readme_table: true

          # Logs debugging info to console.
          # Default is shown.
          debug: false
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

### Run Manually via Docker

Homebrew Releaser does not clean up artifacts after completing since the temporary Docker image on GitHub Actions will be discarded anyway.

**Note:** All environment variables from above must be prepended with `INPUT_` for the local Docker image (eg: `INPUT_SKIP_COMMIT=true`).

```bash
docker-compose up -d --build
```

## Attribution

* Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
