FROM tensorflow/tensorflow:1.12.0-gpu-py3

EXPOSE 8888
EXPOSE 8080

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip install numpy
RUN pip install scipy
RUN pip install sklearn
RUN pip install tensorflow-gpu
RUN pip install feedparser
RUN pip install pandas
RUN pip install librosa
RUN pip install keras
RUN pip install tqdm
RUN AIRFLOW_GPL_UNIDECODE=YES AIRFLOW_HOME=~/airflow pip install apache-airflow

