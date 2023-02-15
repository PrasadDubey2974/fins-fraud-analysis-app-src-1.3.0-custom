#! /bin/bash -x

sudo docker run -d -p 8000:8000 --restart always solutions-accelerators/fins-fraud-analysis-app:latest
