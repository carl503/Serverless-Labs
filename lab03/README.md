# Lab 03

## Introduction

In this lab we were given the task to implement a workflow manager from scratch. We decided to use a yaml based orchestration file and write the main logic in javascript with node js. The orchestration file consists of several different parts. First, we have the global settings. Here you can see settings like run tasks with two outputs in parallel or choose a random route and if prewarm should be used. Second, we have our function description. The functions consist of the fowllowing attributes: a name, an url and an output. Occasionally you will also find "input" as an attribut. This attribut will tell a function that if parallel is enabled it should wait for the input of two ore more functions.

## Setup

In order to test our orchestration we decided to define a couple of basic functions. The first function fetches data from mockaroo in json format. The second function takes an array of json objects and sorts the data by the attribute "last_name" alphabetically. The last function takes an array of json objects as well but shuffles the data inside the array. With these functions it is possible to pipe the output from the shuffle function to the sort function and vice versa.