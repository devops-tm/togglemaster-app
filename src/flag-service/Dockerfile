FROM python:3.11.15-alpine AS builder
WORKDIR /build
COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    --prefix=/install \
    -r requirements.txt

# FROM python:3.11-slim
FROM python:3.11.15-alpine

RUN apk update && apk add --no-cache \
    iputils \
    iproute2 \
    traceroute \
    htop \
    netcat-openbsd \
    curl \
    ca-certificates

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .
EXPOSE 8002