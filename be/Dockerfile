FROM python:3.7-alpine

MAINTAINER Travis Clarke

ENV PYTHONUNBUFFERED 1

ARG ROOT_DIR

RUN mkdir -p "/$ROOT_DIR"
WORKDIR "/$ROOT_DIR"

COPY ./Pipfile ./Pipfile.lock ./setup.py ./README.md ./
#COPY ../config/BUILD ./config/

RUN apk add --no-cache bash build-base && \
    pip install pipenv wait-for-it && \
    pipenv install --dev --system --deploy

COPY ./ ./

EXPOSE $BE_PORT

CMD ["make", "start"]
