FROM python:3.9-alpine3.13
LABEL maintainer="samKenpachi011"

ENV PYTHONNUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /pybha && \
    /pybha/bin/pip install --upgrade pip && \
    /pybha/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /pybha/bin/pip install -r requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/pybha/bin:$PATH"

USER django-user