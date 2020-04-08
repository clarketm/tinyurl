FROM node:lts-alpine

MAINTAINER Travis Clarke

ARG ROOT_DIR

RUN mkdir -p "/$ROOT_DIR"
WORKDIR "/$ROOT_DIR"

#COPY ./package.json ./yarn.lock ./README.md ./
COPY ./package.json ./yarn.lock ./
#COPY ../config/BUILD ./config/

RUN apk add --no-cache bash && \
    yarn install --frozen-lockfile && \
    yarn cache clean

COPY ./ ./

RUN yarn build

EXPOSE $FE_PORT

CMD ["yarn", "serve"]
