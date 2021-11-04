# Lab 04

## Installation

In order to use parts of this program locally, you need to create a 
virtualenv by executing the following command 
```python3 -m venv movie_recommender```. Followed by activating the virtualenv ```source ./movie_recommender/bin/source``` and installing the dependencies by executing ```pip3 install -r requirements.txt```. 

## Introduction

In this lab we decided to implement the requirement R1, R2 and R8.
Because of requirements R1 and R2 we had to use the AWS services from Amazon instead
of Google Cloud Functions. This was quite a challenge for us, because nobody in our
group has ever worked with AWS services before. The biggest three issues were the
quirks of DynamoDB, the permission system IAM and the maximum output size in the state machine.

## Implementation

### R1 - Deployment Framework

We decided to use Zappa as our deployment framework. Zappa fits our needs perfectly, because our recommender is written entirely in Python. The usage of Zappa
was fairly straight forward. We started by deploying our api. Later on in the project we had to provide more information to zappa because we encountered cors and
permission violations. But after fiddeling with the settings and reading a couple of documentations we achieved our goal to deploy the api fully automatically. 

### R2 - Workflow

As Workflow engine we used AWS Step Functions. Inside the step functions we declared a new state machine. Afterwards we began to split up our recommender system in to multiple 
small microservices. Each microservice takes a json input and outputs its result in json as well. There were some complications during this microservice split up process. 
Some of our microservice functions generated output that is simply too large to pass it on as result. So we had to use a little trick and store some of the data inside a s3 bucket. Eventually we were able to successfully replicate our original recommender system by using only microservices. The following image shows the setup.

To deploy our microservices efficiently we decided to abuse zappa and add our microservices as deployment stages. The naming scheme might be quite confusing because every stage is named testX where x stands for an integer that was increased by one for each stage. We had quite a hard time to get the step functions working correctly. 
Therefore we used test functions but never actually changed the naming scheme.

But nevertheless we managed to make it fully funtional and our frontend can now send
a json post request like: ```{"movieID": "1234", "user":"abby", "rating": 6}``` to the state machine and receives an executionArn. This executionArn can then be polled via an api endpoint. When the state machine completes the result will be returned. More about that in R8.

![State Machine](imgs/stepfunctions_graph.svg)
