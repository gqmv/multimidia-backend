# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install dependencies.
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y gettext

# Copy local code to the container image.
COPY . .

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080

# Setting this ensures print statements and log messages
# promptly appear in Cloud Logging.
ENV PYTHONUNBUFFERED TRUE

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 src.core.wsgi:application
