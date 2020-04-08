FROM python:3.7-alpine

MAINTAINER Travis Clarke

ARG ROOT_DIR

RUN mkdir -p "/$ROOT_DIR"
WORKDIR "/$ROOT_DIR"

COPY ./package.json ./yarn.lock ./README.md ./
#COPY ../config/BUILD ./config/

RUN apk add --no-cache bash && \
    yarn install --frozen-lockfile && \
    yarn cache clean

COPY .. ./

EXPOSE $FE_PORT

CMD ["yarn", "start"]
