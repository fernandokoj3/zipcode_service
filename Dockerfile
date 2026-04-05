FROM python:3.13-slim AS builder
LABEL authors="Luis Fernando"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/base.txt .

RUN pip install --prefix=/install --no-cache-dir -r base.txt

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV USER_IMG=zipcode-service

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system ${USER_IMG}-group && \
    adduser --system --ingroup ${USER_IMG}-group ${USER_IMG}

COPY --from=builder /install /usr/local
COPY --chown=${USER_IMG}:${USER_IMG}-group . /app

USER ${USER_IMG}

EXPOSE 5000
