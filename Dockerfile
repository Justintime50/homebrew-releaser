FROM homebrew/brew:4.5.6

COPY homebrew_releaser /tmp/homebrew_releaser
COPY setup.py /tmp/setup.py

RUN brew install python@3.13 \
    && python3 -m venv /tmp/venv \
    && /tmp/venv/bin/pip install .

ENTRYPOINT [ "/tmp/venv/bin/python3", "/tmp/homebrew_releaser/app.py" ]
