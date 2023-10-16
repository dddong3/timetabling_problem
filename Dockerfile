FROM python:3.10-alpine

WORKDIR /app
COPY . .
RUN pip3 install fastapi uvicorn requests

ARG SSL_CERTIFICATE_PATH
ARG SSL_PRIVATE_KEY_PATH

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", SSL_PRIVATE_KEY_PATH, "--ssl-certfile", SSL_CERTIFICATE_PATH]