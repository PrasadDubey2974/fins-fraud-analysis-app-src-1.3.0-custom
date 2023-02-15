# FINS Payments Fraud Analysis Application

This is a dockerized Python application to analyze a transaction and predict 
whether it is potentially fraudulent.

## Prerequisites

This application requires a synthetic financial data set for fraud detection.
By default is has been developed to use the one available from Kaggle at
https://www.kaggle.com/ealaxi/paysim1.

## Endpoints

- /predict - perform fraud analysis
- /healthcheck - get the health status of the running application

## Fraud ML Model Summary

Algorithm: Gradient Boosted Tree (https://en.wikipedia.org/wiki/XGBoost)
Data: Simulated Payments Data (https://www.kaggle.com/ealaxi/paysim1)

### Features

●	Transaction Amount
●	Payor original balance
●	Payor final balance
●	Payee original balance
●	Payee final balance
●	Transaction type

### Methodology

Trees are good at handling simpler problems with relatively linear divisions 
between data. While a complex model, such as a neural network, might have 
worked, tree models are small and require very little hardware to run once 
built making them an ideal choice for a small microservice. XGBoost also 
showed promise in other research on this problem, so it made sense to 
approach from a similar direction as others. 

XGBoost is an advanced tree algorithm that uses gradient descent to construct 
weak learners in order to optimize the accuracy of our overall model. This
 model shows quite a bit of promise with a 99+% AUPRC score.

### Implementation

The code is implemented in Python behind a Flask API served by WSGI. All of 
the code is isolated within a Docker container for easy deployment and 
integration.

## Container Setup

- Use Dockerfile to build image or run `docker-build.sh` script to build and tag the image.
- Run `docker-run.sh` to deploy the container and setup network ports.
- Use `curl http://localhost:8000/healthcheck` to get health status of the application.
