FROM openjdk:11

WORKDIR /app

COPY ./build/libs/analytics.jar ./
ADD templates ./templates

ENV DB_USER=""
ENV DB_PASS=""
ENV DB_NAME=""
ENV DB_HOST=""
ENV PORT=8080

EXPOSE ${PORT}

ENTRYPOINT ["java", "-jar", "analytics.jar"]