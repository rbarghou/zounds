FROM tensorflow/tensorflow:1.12.0-gpu-py3

EXPOSE 8888

RUN apt-get update
RUN apt-get install -y ffmpeg
RUN pip install librosa
RUN pip install keras
