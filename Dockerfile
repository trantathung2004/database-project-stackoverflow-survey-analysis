# Dockerfile
FROM python:3.12-slim


WORKDIR /app

# Install dependencies, including mysql-client
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && apt-get clean

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/.env app/.env
COPY app/ app/
