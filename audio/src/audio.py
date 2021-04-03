import speech_recognition as sr
from os import path
from pydub import AudioSegment
import urllib.request

with urllib.request.urlopen('http://google.com/') as response:
   html = response.read()

# convert mp3 file to wav                                                       
sound = AudioSegment.from_mp3("example.mp3")
sound.export("example.wav", format="wav")

# transcribe audio file                                                         
AUDIO_FILE = "example.wav"

# use the audio file as the audio source                                        
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file                  

        print("Transcription: " + r.recognize_sphinx(audio))