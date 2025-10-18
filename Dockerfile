FROM homebrew/brew:4.5.6

ENV PATH="/home/linuxbrew/.linuxbrew/opt/python@3.13/libexec/bin:${PATH}" \
    HOMEBREW_NO_AUTO_UPDATE=1 \
    HOMEBREW_NO_INSTALL_CLEANUP=1 \
    HOMEBREW_NO_ENV_HINTS=1 \
    HOMEBREW_NO_ANALYTICS=1

COPY --chown=linuxbrew:linuxbrew homebrew_releaser homebrew_releaser
COPY --chown=linuxbrew:linuxbrew setup.py setup.py

RUN brew install python@3.13 \
    && python3 -m venv /home/linuxbrew/venv \
    && /home/linuxbrew/venv/bin/pip install .

ENTRYPOINT [ "/home/linuxbrew/venv/bin/python3", "/home/linuxbrew/homebrew_releaser/app.py" ]
