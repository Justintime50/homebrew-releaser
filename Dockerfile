FROM homebrew/brew:4.5.6

COPY homebrew_releaser /tmp/homebrew-releaser/homebrew_releaser
COPY setup.py /tmp/homebrew-releaser/setup.py

RUN brew install python@3.13 \
    && python3 -m venv /tmp/homebrew-releaser/venv \
    && /tmp/homebrew-releaser/venv/bin/pip install .

ENTRYPOINT ["/bin/bash", "-c", "cd /tmp && exec /tmp/homebrew-releaser/venv/bin/python3 /tmp/homebrew-releaser/homebrew_releaser/app.py"]
