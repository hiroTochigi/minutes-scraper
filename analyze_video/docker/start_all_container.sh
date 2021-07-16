

# Run this script in analyze_video directory
docker run --name extract_audio -itd -v `pwd`:/analyze moviepy
docker run --name separate_audio -itd -v `pwd`:/analyze separate_audio
docker run --name transcript_audio -itd -v `pwd`:/analyze deepspeech
docker run --name deepspeech_pytorch_next -it -v `pwd`:/analyze deepspeech_pytorch:next

# Download deepspeech models
#curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm 
#curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer 
#curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/audio-0.9.3.tar.gz 
#tar xvf audio-0.9.3.tar.gz