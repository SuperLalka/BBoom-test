FROM python:3.9.17-slim-buster

ENV PYTHONUNBUFFERED 1

COPY ./bboom_test /app
COPY poetry.lock pyproject.toml /app/

COPY ./compose/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app

RUN pip install poetry

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
