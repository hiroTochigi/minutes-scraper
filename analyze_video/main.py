import subprocess
import time

start = time.time()
subprocess.run(['docker', 'exec', '-it', 'extract_audio', 'python', 'analyze/src/extract_audio.py'])
subprocess.run(['docker', 'exec', '-it', 'separate_audio', 'python', 'analyze/src/separate_audio.py'])
subprocess.run(['docker', 'exec', '-it', 'transcript_audio', 'python', 'analyze/src/transcript.py'])
end = time.time()

print(end - start)