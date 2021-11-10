FROM ubuntu:focal

ENV DB_USER=""
ENV DB_PASS=""
ENV DB_NAME=""
ENV DB_HOST=""
ENV PORT=8080

WORKDIR /app
COPY * ./

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs npm
RUN npm i

EXPOSE $PORT

ENTRYPOINT ["node", "."]