FROM python:3.12-alpine

WORKDIR /app

COPY pyproject.toml /app/
COPY poetry.lock /app/
COPY . /app/
ENV PYTHONPATH=/app
WORKDIR /app/src

RUN pip install poetry
RUN poetry install --no-root
