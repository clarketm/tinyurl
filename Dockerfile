FROM python:3.7-alpine

MAINTAINER Travis Clarke

ENV PYTHONUNBUFFERED 1

ARG ROOT_DIR

RUN mkdir -p "/$ROOT_DIR"
WORKDIR "/$ROOT_DIR"

COPY ./Pipfile ./Pipfile.lock ./setup.py ./README.md ./
COPY ./config/BUILD ./config/

RUN apk add --no-cache bash git build-base jpeg-dev zlib-dev && \
    pip install pipenv wait-for-it && \
    pipenv install --dev --system --deploy

COPY ./ ./

EXPOSE 8000

CMD ["make", "start"]
