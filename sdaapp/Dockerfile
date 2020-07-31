# Get base image using miniconda
FROM puckel/docker-airflow:1.10.1 

# set environment vars

# Setup requirements.txt
COPY requirements.txt /app/

# Installs, clean, and update
#RUN   pip install --upgrade apache-airflow
RUN   pip install -r /app/requirements.txt
