FROM python:3.9.6-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y curl

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root

COPY . /app/

RUN chmod +x /app/bash_commands/startup.sh

#RUN chmod +x /app/bash_commands/create-multiple-postgresql-databases.sh
#ARG ENVIRONMENT=dev
#RUN bash -c "if [ $ENVIRONMENT == "dev" ] || [ $ENVIRONMENT == "test" ]; then pip3 install -r requirements-dev.txt ; else pip3 install -r requirements.txt ; fi"
