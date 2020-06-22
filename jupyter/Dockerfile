# Get base image using miniconda
#FROM jupyter/datascience-notebook:latest
#FROM continuumio/miniconda3:latest
FROM jupyter/scipy-notebook

# set environment vars
ENV ACCEPT_INTEL_PYTHON_EULA=yes


# Setup requirements.txt
COPY requirements.txt /app/

# Installs, clean, and update
#RUN  conda install --quiet --yes --file /app/requirements.txt
RUN   pip install -r /app/requirements.txt
#    && apt-get update \
#    && apt-get clean \
#    && apt-get update -qqq \
#    && apt-get install -y -q g++ \
#    && conda install --yes --file /app/requirements.txt
#    && pip install -r /app/requirements.txt
#    && conda config --add channels intel  \
#    && conda install -y -q intelpython2_full=2018.0.1 python=2 \
#    && pip install --upgrade pip \
#    && pip install -r /app/requirements.txt

#RUN conda install --yes --file /app/requirements.txt
#RUN conda install --yes --file /tmp/requirements.txt && \
#    fix-permission $CONDA_DIR && \
#    fix-permission /home/$NB_USER

#ENTRYPOINT ["jupyter","lab","--ip=0.0.0.0","--allow-root"]
#ENTRYPOINT ["bash"]
#CMD tail -f /dev/null

#CMD jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root
