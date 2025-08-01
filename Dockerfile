FROM homebrew/brew:4.5.6

COPY --chown=linuxbrew:linuxbrew homebrew_releaser homebrew_releaser
COPY --chown=linuxbrew:linuxbrew setup.py setup.py

RUN brew install python@3.13 \
    && python3 -m venv /home/linuxbrew/venv \
    && /home/linuxbrew/venv/bin/pip install .

ENTRYPOINT [ "/home/linuxbrew/venv/bin/python3", "/home/linuxbrew/homebrew_releaser/app.py" ]
