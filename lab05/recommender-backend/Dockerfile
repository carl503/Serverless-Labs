FROM ubuntu:focal

ENV DB_USER=""
ENV DB_PASS=""
ENV DB_NAME=""
ENV DB_HOST=""
ENV PORT=8080

WORKDIR /app
COPY * ./

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

EXPOSE $PORT

ENTRYPOINT [ "python3", "app.py" ]
