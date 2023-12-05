PYTHON_BINARY := "python3"
VIRTUAL_ENV := "venv"
VIRTUAL_BIN := VIRTUAL_ENV / "bin"
PROJECT_NAME := "homebrew_releaser"
TEST_DIR := "test"
CURRENT_DIR := `pwd`

# Runs brew audit against the generated formula
audit:
    #!/usr/bin/env bash
    brew tap-new homebrew-releaser/test --no-git
    cp -r test/formulas/* $(brew --repository)/Library/Taps/homebrew-releaser/homebrew-test/Formula
    cp -r test/formula_imports $(brew --repository)/Library/Taps/homebrew-releaser/homebrew-test
    for file in $(brew --repository)/Library/Taps/homebrew-releaser/homebrew-test/Formula/*
    do
        brew audit --formula "homebrew-releaser/test/$(basename ${file%.rb})"
    done
    brew untap homebrew-releaser/test

# Scans the project for security vulnerabilities
bandit:
    {{VIRTUAL_BIN}}/bandit -r {{PROJECT_NAME}}/

# Runs the Black Python formatter against the project
black:
    {{VIRTUAL_BIN}}/black {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Checks if the project is formatted correctly against the Black rules
black-check:
    {{VIRTUAL_BIN}}/black {{PROJECT_NAME}}/ {{TEST_DIR}}/ --check

# Test the project and generate an HTML coverage report
coverage:
    {{VIRTUAL_BIN}}/pytest --cov={{PROJECT_NAME}} --cov-branch --cov-report=html --cov-report=lcov --cov-report=term-missing --cov-fail-under=95

# Remove the virtual environment and clear out .pyc files
clean:
    rm -rf {{VIRTUAL_ENV}} dist *.egg-info .coverage htmlcov .*cache
    find . -name '*.pyc' -delete

# Lints the project
lint: black-check isort-check flake8 mypy bandit

# Fixes lint issues
lint-fix: black isort

# Install the project locally
install:
    {{PYTHON_BINARY}} -m venv {{VIRTUAL_ENV}}
    {{VIRTUAL_BIN}}/pip install -e ."[dev]"

# Sorts imports throughout the project
isort:
    {{VIRTUAL_BIN}}/isort {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Checks that imports throughout the project are sorted correctly
isort-check:
    {{VIRTUAL_BIN}}/isort {{PROJECT_NAME}}/ {{TEST_DIR}}/ --check-only

# Run flake8 checks against the project
flake8:
    {{VIRTUAL_BIN}}/flake8 {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Run mypy type checking on the project
mypy:
    {{VIRTUAL_BIN}}/mypy {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Test the project
test:
    {{VIRTUAL_BIN}}/pytest
