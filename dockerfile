FROM python:3

WORKDIR /app

COPY src .

# Ignore warnings from pip and python, solution is based on default versions
# Upgrading either may lead to the retrain step failing
RUN pip3 install -r requirements.txt
RUN pip install -U scikit-learn
# Disable these steps if you do not have a simulated_data.csv file from
# https://www.kaggle.com/ealaxi/paysim1 available
RUN python3 retrain.py
RUN rm SimulatedData.csv

EXPOSE 8000

# start the app
ENTRYPOINT ["/bin/sh", "./startup.sh"]