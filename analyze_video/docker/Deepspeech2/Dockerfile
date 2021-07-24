# set base image (host OS)
FROM python:bionic

RUN apt update && apt install -y \ 
    sox \
    pkg-config \
    libflac-dev \
    libogg-dev \
    libvorbis-dev \
    libboost-dev \
    swig \
    python3-dev

#RUN git clone https://github.com/PaddlePaddle/DeepSpeech.git && \
#    cd DeepSpeech && \
#    pushd tools; make; popd && \
#    source tools/venv/bin/activate && \
#    bash setup.sh
