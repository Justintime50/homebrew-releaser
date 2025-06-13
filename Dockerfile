FROM homebrew/brew:4.5.6

WORKDIR /github/workspace

COPY homebrew_releaser homebrew_releaser
COPY setup.py setup.py

RUN brew install python@3.13 \
    && python3 -m venv venv \
    && venv/bin/pip install .

ENTRYPOINT [ "venv/bin/python3", "homebrew_releaser/app.py" ]
