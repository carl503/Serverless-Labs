FROM node:lts-slim

LABEL org.opencontainers.image.authors="albreaus@students.zhaw.ch, lubojcar@students.zhaw.ch, meletlea@students.zhaw.ch"

ENV MONGO_URL=""
ENV PORT=""

WORKDIR /app
COPY * ./

RUN npm i

ENTRYPOINT ["node", "api.js"]