# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY ./src /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Select the file to run
ENV MAIN_FILE navigation.py
ENV PORT 8501
EXPOSE $PORT

ENV PATH_FROM_ROOT /

# CMD [ "/bin/sh", "-c", "echo", "${MAIN_FILE}" ]
CMD [ "/bin/sh", "-c", " exec streamlit run /app/${MAIN_FILE} --server.port=${PORT} --server.address=0.0.0.0 --server.headless=TRUE --browser.gatherUsageStats=FALSE" ]
