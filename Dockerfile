# syntax=docker/dockerfile:1
FROM python:3.12-slim
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


WORKDIR /app
COPY ./src /app/src

# Install pip requirements
COPY pyproject.toml .
RUN uv venv
RUN uv pip install .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Select the file to run
ENV MAIN_FILE main.py
ENV PORT 8501
EXPOSE $PORT

ENV PATH_FROM_ROOT /

# CMD [ "/bin/sh", "-c", "echo", "${MAIN_FILE}" ]
CMD [ "/bin/sh", "-c", " exec uv run streamlit run /app/src/${MAIN_FILE} --server.port=${PORT} --server.address=0.0.0.0 --server.headless=TRUE --browser.gatherUsageStats=FALSE --client.toolbarMode=minimal --client.showErrorDetails=none --client.showErrorLinks=False " ]
