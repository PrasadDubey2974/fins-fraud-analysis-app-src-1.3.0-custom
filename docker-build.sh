#!/bin/bash -x

sudo docker build -f Dockerfile -t solutions-accelerators/fins-fraud-analysis-app .
sudo docker tag solutions-accelerators/fins-fraud-analysis-app:latest solutions-accelerators/fins-fraud-analysis-app:1.3.0
