FROM python:3.11-slim-bullseye AS builder

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry 

RUN poetry config virtualenvs.create true

RUN poetry config virtualenvs.in-project true

RUN poetry install --without dev --no-interaction --no-ansi 

FROM python:3.11-slim-bullseye AS app

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src:$PYTHONPATH

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src /app/src

COPY data /app/data

RUN mkdir -p /app/data/results

RUN mkdir -p /var/log/uvicorn

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]

EXPOSE 8080