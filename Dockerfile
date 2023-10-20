FROM python:3.10-alpine

WORKDIR /app
COPY . .

RUN pip3 install fastapi uvicorn requests
ENTRYPOINT uvicorn server:app --host 0.0.0.0 --port 443 --ssl-certfile ssl_pub_key.pem --ssl-keyfile ssl_priv_key.pem