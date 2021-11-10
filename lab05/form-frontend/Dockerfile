FROM ubuntu:focal

ENV DB_USER=
ENV DB_PASS=
ENV DB_NAME=
ENV DB_HOST=
ENV PORT=

RUN mkdir /app
COPY * /app

WORKDIR /app
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs npm
RUN npm i

ENTRYPOINT ["node", "."]