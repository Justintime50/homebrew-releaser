FROM python:3.9
# TODO: See if we can use a smaller Python image that still contains the tools we need

COPY ./setup.py /setup.py
COPY ./README.md /README.md
COPY ./shell_releaser /shell_releaser

RUN pip install -e .

ENTRYPOINT [ "python", "/shell_releaser/releaser.py" ]
