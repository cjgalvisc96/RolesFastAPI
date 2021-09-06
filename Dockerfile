FROM python:3.9.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app/

COPY . /app/

RUN chmod +x /app/bash_commands/startup.sh
RUN pip3 install -r /app/requirements/requirements-dev.txt

#RUN chmod +x /app/bash_commands/create-multiple-postgresql-databases.sh
#ARG ENVIRONMENT=dev
#RUN bash -c "if [ $ENVIRONMENT == "dev" ] || [ $ENVIRONMENT == "test" ]; then pip3 install -r requirements-dev.txt ; else pip3 install -r requirements.txt ; fi"
