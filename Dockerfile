FROM homebrew/brew:4.5.6

WORKDIR /home/linuxbrew/homebrew-releaser

COPY --chown=linuxbrew:linuxbrew homebrew_releaser homebrew_releaser
COPY --chown=linuxbrew:linuxbrew setup.py setup.py

RUN brew install python@3.13 \
    && python3 -m venv /home/linuxbrew/homebrew-releaser/venv \
    && /home/linuxbrew/homebrew-releaser/venv/bin/pip install .

ENTRYPOINT [ "/home/linuxbrew/homebrew-releaser/venv/bin/python3", "/home/linuxbrew/homebrew-releaser/homebrew_releaser/app.py" ]
