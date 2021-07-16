FROM python:bionic

WORKDIR /analyze

RUN apt-get update && \
    apt-get install -y --no-install-recommends libsndfile1 sox

RUN pip install torch==1.9.0+cpu \
        torchvision==0.10.0+cpu \
        torchaudio==0.9.0 \
        -f https://download.pytorch.org/whl/torch_stable.html

COPY requirements.txt ./

RUN pip install -r requirements.txt
