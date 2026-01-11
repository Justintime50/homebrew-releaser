import os


# GitHub Action Parameters
HOMEBREW_OWNER = os.getenv("INPUT_HOMEBREW_OWNER", "").lower()
HOMEBREW_TAP = os.getenv("INPUT_HOMEBREW_TAP", "").lower()
FORMULA_FOLDER = os.getenv("INPUT_FORMULA_FOLDER", "Formula")
GITHUB_TOKEN = os.getenv("INPUT_GITHUB_TOKEN")
COMMIT_OWNER = os.getenv("INPUT_COMMIT_OWNER", "homebrew-releaser")
COMMIT_EMAIL = os.getenv("INPUT_COMMIT_EMAIL", "homebrew-releaser@example.com")
DEPENDS_ON = os.getenv("INPUT_DEPENDS_ON")
INSTALL = os.getenv("INPUT_INSTALL")
TEST = os.getenv("INPUT_TEST")
DOWNLOAD_STRATEGY = os.getenv("INPUT_DOWNLOAD_STRATEGY")
CUSTOM_REQUIRE = os.getenv("INPUT_CUSTOM_REQUIRE")
FORMULA_INCLUDES = os.getenv("INPUT_FORMULA_INCLUDES")
UPDATE_PYTHON_RESOURCES = (
    os.getenv("INPUT_UPDATE_PYTHON_RESOURCES", False)
    if os.getenv("INPUT_UPDATE_PYTHON_RESOURCES") != "false"
    else False
)
VERSION = os.getenv("INPUT_VERSION")
TARGET_DARWIN_AMD64 = (
    os.getenv("INPUT_TARGET_DARWIN_AMD64", False) if os.getenv("INPUT_TARGET_DARWIN_AMD64") != "false" else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string
TARGET_DARWIN_ARM64 = (
    os.getenv("INPUT_TARGET_DARWIN_ARM64", False) if os.getenv("INPUT_TARGET_DARWIN_ARM64") != "false" else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string
TARGET_LINUX_AMD64 = (
    os.getenv("INPUT_TARGET_LINUX_AMD64", False) if os.getenv("INPUT_TARGET_LINUX_AMD64") != "false" else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string
TARGET_LINUX_ARM64 = (
    os.getenv("INPUT_TARGET_LINUX_ARM64", False) if os.getenv("INPUT_TARGET_LINUX_ARM64") != "false" else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string
CUSTOM_TARBALL = os.getenv("INPUT_CUSTOM_TARBALL")
UPDATE_README_TABLE = (
    os.getenv("INPUT_UPDATE_README_TABLE", False) if os.getenv("INPUT_UPDATE_README_TABLE") != "false" else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string
SKIP_COMMIT = (
    os.getenv("INPUT_SKIP_COMMIT", False) if os.getenv("INPUT_SKIP_COMMIT") != "false" else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string
SKIP_CHECKSUM = (
    os.getenv("INPUT_SKIP_CHECKSUM", False) if os.getenv("INPUT_SKIP_CHECKSUM") != "false" else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string
DEBUG = (
    os.getenv("INPUT_DEBUG", False) if os.getenv("INPUT_DEBUG") != "false" else False
)  # Must check for string `false` since GitHub Actions passes the bool as a string

# App Constants
LOGGER_NAME = "homebrew-releaser"
TIMEOUT = 300
GITHUB_BASE_URL = "https://github.com"
GITHUB_BASE_API_URL = "https://api.github.com"
GITHUB_HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Agent": "Homebrew Releaser",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
}
CHECKSUM_FILE = "checksum.txt"
WORKING_DIR = os.path.join(os.sep, "app")

# Formula Constants
ARTICLES = {
    "a",
    "an",
    "the",
}
MAX_DESC_FIELD_LENGTH = 80  # `brew audit` wants no more than 80 characters in the desc field

# GitHub Action env variables set by GitHub
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "user/repo").split("/")
GITHUB_OWNER = GITHUB_REPOSITORY[0]
GITHUB_REPO = GITHUB_REPOSITORY[1]
