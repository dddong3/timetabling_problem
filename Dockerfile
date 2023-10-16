FROM python:3.10-alpine

WORKDIR /app
COPY . .
RUN pip3 install fastapi uvicorn requests

ARG SSL_PUB_KEY
ARG SSL_PRIV_KEY
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "443", "--ssl-certfile", SSL_PUB_KEY, "--ssl-keyfile", SSL_PRIV_KEY]