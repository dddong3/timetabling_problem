FROM python:3.10-slim-bullseye as builder

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry 

RUN poetry config virtualenvs.create true

RUN poetry config virtualenvs.in-project true

RUN poetry install --without dev --no-interaction --no-ansi 

FROM python:3.10-slim-bullseye as app

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src:$PYTHONPATH

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN apt-get update && apt-get install -y nginx supervisor

RUN rm -rf /etc/nginx/sites-enabled/default

COPY deploy/conf/nginx.conf /etc/nginx/conf.d/default.conf

COPY src /app/src

COPY data /app/data

RUN mkdir -p /app/data/results

COPY deploy/conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN mkdir -p /var/log/supervisor /var/log/nginx /var/log/uvicorn

CMD [ "supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

EXPOSE 80
