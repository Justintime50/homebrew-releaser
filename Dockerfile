FROM python:3.12-alpine

RUN apk add --no-cache \
    # Install git to push new Homebrew formula
    git \
    # Install perl-utils for `shasum` tool to get tar archive checksums
    perl-utils

COPY . .

RUN pip install -e .

ENTRYPOINT [ "python", "/homebrew_releaser/app.py" ]
