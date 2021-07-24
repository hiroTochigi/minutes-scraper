#!/bin/bash

deepspeech_pytorch_src_dir="src/deepspeech_pytorch/deepspeech.pytorch/"
is_deepspeech_installed=`expr length "$(pip list | grep deepspeech-pytorch)"`

if [ ! -d "transcript" ]
then
  mkdir "transcript"
fi

if [ ! -d $deepspeech_pytorch_src_dir ]
then
  cd $deepspeech_pytorch_src_dir
  git clone https://github.com/hiroTochigi/deepspeech.pytorch
  cd /analyze
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
  cd $deepspeech_pytorch_src_dir
  pip install -e . # Dev install
  cd /analyze
fi

cp src/deepspeech_pytorch/run.py "${deepspeech_pytorch_src_dir}run.py" 
chmod +x "${deepspeech_pytorch_src_dir}run.py"

python "${deepspeech_pytorch_src_dir}run.py"