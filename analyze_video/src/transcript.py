from deepspeech import Model
import numpy as np
import os
import wave
import shlex
import subprocess
from pydub import AudioSegment

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

model_file_path = '/analyze/model/deepspeech-0.9.3-models.pbmm'
lm_file_path = '/analyze/model/deepspeech-0.9.3-models.scorer'

beam_width = 500
lm_alpha = 0.93
lm_beta = 1.18

model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)

model.setScorerAlphaBeta(lm_alpha, lm_beta)
model.setBeamWidth(beam_width)

def read_wav_file(filename):
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)
        print(rate)
        print(frames)

    return buffer, rate

def transcribe(filename):
   buffer, rate = read_wav_file(filename)
   desired_sample_rate = model.sampleRate()
   if desired_sample_rate != rate:
       return model.stt(convert_samplerate(filename, desired_sample_rate))
   data16 = np.frombuffer(buffer, dtype=np.int16)
   return model.stt(data16)

def convert_samplerate(audio_path, desired_sample_rate):
    sox_cmd = 'sox {}  --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(quote(audio_path), desired_sample_rate)
    #sox_cmd = 'sox {} --type raw -r {} - '.format(quote(audio_path), 16000)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use {}hz files or install it: {}'.format(desired_sample_rate, e.strerror))

    print(np.frombuffer(output, np.int16))
    print(len(np.frombuffer(output, np.int16)))
    return np.frombuffer(output, np.int16)

def check_or_make_dir(audio_dir):

    if not os.path.isdir(audio_dir):
        os.mkdir(audio_dir)

for (root,dirs,files) in os.walk('/analyze/audio/output'):
    for audio_file in files:
        output_dir = root.replace('audio/output', 'transcript')
        check_or_make_dir(output_dir)   
        result = ''
        if audio_file.find('mp3') > -1:
            output = f"{audio_file.split('.')[0]}.wav"
            subprocess.call(['ffmpeg', '-i', f'{root}/{audio_file}',
                  f'{root}/{output}'])
            result = transcribe(f"{root}/{output}")
            os.remove(f'{root}/{audio_file}')
        elif audio_file.find('wav') > -1:
            result = transcribe(f"{root}/{audio_file}")
        
        with open(f'{output_dir}/{audio_file.split(".")[0]}.txt', 'w') as w:
            print(result)
            w.write(result)
        

