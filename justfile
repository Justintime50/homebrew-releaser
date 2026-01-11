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

# Test the project and generate an HTML coverage report
coverage:
    {{VIRTUAL_BIN}}/pytest --cov={{PROJECT_NAME}} --cov-branch --cov-report=html --cov-report=lcov --cov-report=term-missing --cov-fail-under=90

# Remove the virtual environment and clear out .pyc files
clean:
    rm -rf {{VIRTUAL_ENV}} dist *.egg-info .coverage htmlcov .*cache
    find . -name '*.pyc' -delete

# Lints the project
lint:
    {{VIRTUAL_BIN}}/ruff check {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Fixes lint issues
lint-fix:
    {{VIRTUAL_BIN}}/ruff check --fix {{PROJECT_NAME}}/ {{TEST_DIR}}/
    {{VIRTUAL_BIN}}/ruff format {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Install the project locally
install:
    {{PYTHON_BINARY}} -m venv {{VIRTUAL_ENV}}
    {{VIRTUAL_BIN}}/pip install -e ."[dev]"

# Run mypy type checking on the project
mypy:
    {{VIRTUAL_BIN}}/mypy --install-types --non-interactive {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Test the project
test:
    {{VIRTUAL_BIN}}/pytest
