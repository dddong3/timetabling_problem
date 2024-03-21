FROM python:3.10-slim-bullseye as builder

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry 

RUN poetry config virtualenvs.create true

RUN poetry config virtualenvs.in-project true

RUN poetry install --without dev --no-interaction --no-ansi 

FROM python:3.10-slim-bullseye as app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src:$PYTHONPATH

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src /app/src

COPY data /app/data

RUN mkdir -p /app/data/results

CMD ["uvicorn", "src.app:app", "--host", "127.0.0.1", "--port", "80"]

EXPOSE 80
