# Lab 03

## Introduction

In this lab we were given the task to implement a workflow manager from scratch. We decided to use a yaml based orchestration file and write the main logic in javascript with node js. The orchestration file consists of several different parts. First, we have the global settings. Here you can see settings like run tasks with two outputs in parallel or choose a random route and if prewarm should be used. Second, we have our function description. The functions consist of the fowllowing attributes: a name, an url and an output. Occasionally you will also find "input" as an attribut. This attribut will tell a function that if parallel is enabled it should wait for the input of two ore more functions.

## Setup

In order to test our orchestration we decided to define a couple of basic functions. The first function fetches data from mockaroo in json format. The second function takes an array of json objects and sorts the data by the attribute "last_name" alphabetically. The last function takes an array of json objects as well but shuffles the data inside the array. With these functions it is possible to pipe the output from the shuffle function to the sort function and vice versa.

## Results

We tested our workflow manager by measuring the full execution from the first to the last function for 300 times. One time without and one time with warmup enabled. 
Without the warmup we measured function execution time in ms: 

|      | Function 0 | function 1 | function 2 | function 3 | function 4 |
| ---- | ---------- | ---------- | ---------- | ---------- | ---------- |
| Min  | 71         | 112        | 111        | 112        | 115        |
| Max  | 203        | 1128       | 227        | 283        | 293        |
| Avg  | 89.65      | 148.14     | 130.28     | 131.70     | 141.93     |

Withe the warmup we measured:

|      | Function 0 | Function 1 | Function 2 | Function 3 | Function 4 |
| ---- | ---------- | ---------- | ---------- | ---------- | ---------- |
| Min  | 73         | 117        | 111        | 115        | 111        |
| Max  | 220        | 1195       | 355        | 336        | 363        |
| Avg  | 91.91      | 148.82     | 132.86     | 135.01     | 146.79     |

This is quite surprising for us. Even with a prewarmup the average and the max times are not lower but slightly higher. We are not entirely sure why this is happening.