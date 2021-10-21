# Lab 03

## Introduction

In this lab we were given the task to implement a workflow manager from scratch. We decided to use a yaml based orchestration file and write the main logic in javascript with node js. The orchestration file consists of several different parts. First, we have the global settings. Here you can see settings like run tasks with two outputs in parallel or choose a random route and if prewarm should be used.

Example:
```yml
orchestrator:
  prewarm: false
  isParallel: false
```

Second, we have our function description. The functions consist of the fowllowing attributes: a name, an url and an output. Occasionally you will also find "input" as an attribute. This attribute will tell a function that if parallel is enabled it should wait for the input of two ore more functions.

Example:
```yml
  functions:
    f0:
      name: "Function 0"
      url: "https://europe-west6-scad-zhaw.cloudfunctions.net/lab03-f0"
      output:
        - f1
```

## Setup

In order to test our orchestration we decided to define a couple of basic functions. 
The first function fetches data from [mockaroo](https://mockaroo.com/) in json format.
The second function takes an array of json objects and sorts the data by the "last_name" attribute alphabetically.
The last function takes an array of json objects as well but shuffles the data inside the array. With these functions it is possible to pipe the output from the shuffle function to the sort function and vice versa.

## Results

We tested our workflow manager by measuring the full execution from the first to the last function for 300 times. One time without and one time with warmup enabled. 
Without the warmup we measured function execution time in ms: 

|      | Function 0 | function 1 | function 2 | function 3 | function 4 |
| ---- | ---------- | ---------- | ---------- | ---------- | ---------- |
| Min  | 89         | 132        | 136        | 130        | 131        |
| Max  | 3906       | 1279       | 1846       | 1241       | 1313       |
| Avg  | 121.54     | 189.30     | 231.32     | 203.09     | 167.00     |

Withe the warmup we measured:

|      | Function 0 | Function 1 | Function 2 | Function 3 | Function 4 |
| ---- | ---------- | ---------- | ---------- | ---------- | ---------- |
| Min  | 73         | 117        | 111        | 115        | 111        |
| Max  | 220        | 1195       | 355        | 336        | 363        |
| Avg  | 91.91      | 148.82     | 132.86     | 135.01     | 146.79     |

As we can see warmup can make quite an impact. 
With the warmup enabled we were able to reduce the max and average timings quite a lot.