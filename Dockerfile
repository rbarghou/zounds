FROM tensorflow/tensorflow:1.12.0-gpu-py3

EXPOSE 8888
EXPOSE 8080

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip install numpy scipy sklearn tensorflow-gpu feedparser \
  pandas librosa keras tqdm
RUN pip3 install -U jupyter ipython

RUN AIRFLOW_GPL_UNIDECODE=YES AIRFLOW_HOME=~/airflow pip install apache-airflow

