FROM python:3.10-alpine

WORKDIR /app
COPY . .
RUN pip3 install fastapi uvicorn requests

ENTRYPOINT uvicorn server:app --host 0.0.0.0 --port 443 --ssl-certfile $SSL_PUB_KEY --ssl-keyfile $SSL_PRIV_KEY