FROM python:3.10-alpine
LABEL maintainer="TamarBel"

ENV PYTHONUNBUFFERED=1

RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; \
        then /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp

RUN apk del .tmp-build-deps

COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user
