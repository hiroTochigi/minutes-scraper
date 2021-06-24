# set base image (host OS)
FROM python:latest

# Set up dependencies
RUN apt update && apt install -y \
    ffmpeg \
    sox \
    python \
    python-all-dev \
    python-pip \
    build-essential \
    swig \
    libpulse-dev \
    libasound2-dev 

# install dependencies
RUN pip install deepspeech \
    numpy==1.20.3 \
    pydub==0.25.1 
    

#RUN curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm && \
#    curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer 
#
#RUN curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/audio-0.9.3.tar.gz && \
#    tar xvf audio-0.9.3.tar.gz
