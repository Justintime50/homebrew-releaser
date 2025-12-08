FROM debian:stable-slim

WORKDIR /app

ENV HOMEBREW_NO_AUTO_UPDATE=1 \
    HOMEBREW_NO_INSTALL_CLEANUP=1 \
    HOMEBREW_NO_ENV_HINTS=1 \
    HOMEBREW_NO_ANALYTICS=1

RUN \
    # Setup system dependencies
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential curl git ca-certificates bash && \
    rm -rf /var/lib/apt/lists/* && \
    # Setup Homebrew
    useradd -m linuxbrew && \
    curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | \
        su - linuxbrew -c "NONINTERACTIVE=1 /bin/bash" && \
    su - linuxbrew -c "git -C /home/linuxbrew/.linuxbrew/Homebrew checkout 5.0.4" && \
    chown linuxbrew:linuxbrew /app

USER linuxbrew

ENV PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:${PATH}"

RUN brew install python@3.14

COPY pyproject.toml .
COPY homebrew_releaser homebrew_releaser

RUN python3 -m venv venv && \
    venv/bin/pip install .

ENTRYPOINT ["/app/venv/bin/python", "/app/homebrew_releaser/app.py"]
