FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends git

RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" \
    && echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /etc/profile \
    && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    
COPY homebrew_releaser homebrew_releaser
COPY setup.py setup.py

RUN pip install .

ENTRYPOINT [ "python", "/homebrew_releaser/app.py" ]
