FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive \
    NONINTERACTIVE=1 \
    HOMEBREW_NO_AUTO_UPDATE=1 \
    HOMEBREW_NO_INSTALL_CLEANUP=1 \
    HOMEBREW_NO_ENV_HINTS=1 \
    HOMEBREW_NO_ANALYTICS=1

RUN \
    # Setup system dependencies
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential curl git ca-certificates procps bash && \
    rm -rf /var/lib/apt/lists/* && \
    # Setup Homebrew
    useradd -m linuxbrew && \
    curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | \
        su - linuxbrew -c "NONINTERACTIVE=1 /bin/bash" && \
    chgrp -R root /home/linuxbrew/.linuxbrew && \
    chmod -R g+rX /home/linuxbrew/.linuxbrew;

ENV PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:${PATH}"

COPY pyproject.toml .
COPY homebrew_releaser homebrew_releaser

RUN python3 -m venv /venv \
    && venv/bin/pip install .

ENTRYPOINT ["venv/bin/python3", "homebrew_releaser/app.py"]
