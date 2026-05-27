# syntax=docker/dockerfile:1
FROM python:3.12-slim
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./src /app/src
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN sed -i 's/\r$//' /app/docker-entrypoint.sh

# Install pip requirements
COPY pyproject.toml .
RUN uv venv
RUN uv pip install .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser \
    && mkdir -p /data \
    && chown -R appuser /app /data \
    && chmod +x /app/docker-entrypoint.sh
USER appuser

# Select the file to run
ENV MAIN_FILE=main.py
ENV PORT=8501
EXPOSE $PORT

ENV EDUSPEC_DATA_DIR=/data

# CMD [ "/bin/sh", "-c", "echo", "${MAIN_FILE}" ]
ENTRYPOINT [ "/bin/sh", "/app/docker-entrypoint.sh" ]
CMD [ "/bin/sh", "-c", " exec uv run streamlit run /app/src/${MAIN_FILE} --server.port=${PORT} --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false --client.toolbarMode=viewer --client.showErrorDetails=none --client.showErrorLinks=false " ]
