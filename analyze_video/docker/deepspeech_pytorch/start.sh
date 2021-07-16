#!/bin/bash


is_deepspeech_installed=`expr length "$(pip list | grep deepspeech-pytorch)"`

if [ ! -d "transcript" ]
then
  mkdir "transcript"
fi
if [ ! -d "src/deepspeech.pytorch" ]
then
  cd src
  git clone https://github.com/hiroTochigi/deepspeech.pytorch
  cd ..
fi
if [ ! -f "models/deepspeech.pytorch/librispeech_pretrained_v3.ckpt" ]
then
  if [ ! -d "models/deepspeech.pytorch" ]
  then
    mkdir -p models/deepspeech.pytorch/
  fi
  cd models/deepspeech.pytorch/
  wget https://github.com/SeanNaren/deepspeech.pytorch/releases/download/V3.0/librispeech_pretrained_v3.ckpt
  cd /analyze
fi
if [ $is_deepspeech_installed -eq 0 ]
then
  cd deepspeech.pytorch/
  pip install -e . # Dev install
  cd ..
fi

python deepspeech.pytorch/run.py