FROM python:3.10-alpine

WORKDIR /app
COPY . .

RUN pip3 install fastapi uvicorn requests
ENTRYPOINT uvicorn server:app --host 0.0.0.0 --port 443 --ssl-certfile cert1.pem --ssl-keyfile privkey1.pem