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
RUN apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

EXPOSE $PORT

ENTRYPOINT [ "python3", "app.py" ]
