FROM python:3.9-alpine

RUN apk add --no-cache \
    # Install git to push new Homebrew formula
    git \
    # Install perl-utils for `shasum` tool to get tar archive checksums
    perl-utils

COPY ./setup.py /setup.py
COPY ./README.md /README.md
COPY ./homebrew_releaser /homebrew_releaser

RUN pip install -e .

ENTRYPOINT [ "python", "/homebrew_releaser/releaser.py" ]
