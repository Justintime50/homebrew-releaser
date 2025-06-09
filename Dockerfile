FROM homebrew/brew

WORKDIR /home/linuxbrew/homebrew-releaser

COPY --chown=linuxbrew:linuxbrew homebrew_releaser homebrew_releaser
COPY --chown=linuxbrew:linuxbrew setup.py setup.py

RUN brew install python@3.13 \
    && python3 -m venv venv \
    && venv/bin/pip3 install .

ENTRYPOINT [ "venv/bin/python3", "homebrew_releaser/app.py" ]
