# Lab 06

## Introduction

In this lab we had the task to use a programming language or a framework, which was specifically made for microservice development and combine it with an SDL and/or IDL. 

We chose Ballerina, because it seemed like a straight forward microservice framework, which uses the JVM. Ballerina fits our purpose perfectly. We decided to create FizzbuzzaaS. The user interacts with the program via a query parameter in which he or she provides the limit to generate FizzBuzz. For instance, if the user wishes to generate FizzBuzz with an amount of 100 the program will play FizzBuzz from 0 to 100. The user receives the FizzBuzz output as well as some statistics to the generated FizzBuzz output.

## SDL

Thanks to Ballerinas build in OpenAPI it was quite easy to create the needed services. In each corresponding microservice folder the OpenAPI description for the main entry point can be found.

## Usage

In order to use the Program you just have to run docker-compose up. Then you should visit [FizzBuzz](http://localhost:9090/fizzbuzz?amount=100). The default Port for the main entry point is 9090 but can be easily changed in the docker-compose file.