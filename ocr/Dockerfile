# set base image (host OS)
FROM python:latest

# set the working directory in the container
WORKDIR /code

# Set up dependencies
RUN apt update && apt install -y \
    python \
    python-all-dev \
    python-pip \
    build-essential \
    libpulse-dev \
    libasound2-dev 

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python", "./audio.py" ]