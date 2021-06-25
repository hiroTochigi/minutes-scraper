import os
import subprocess

video_dir = '/analyze/video/'
audio_dir = '/analyze/audio/input/'

def main():
    for (root,dirs,video_file_list) in os.walk(f'{video_dir}'):
        for video_file in video_file_list:
            audio_file = f'{"".join(video_file.split(".")[:-1])}.mp3'
            subprocess.run(['ffmpeg', '-i', f'{video_dir}{video_file}', '-q:a', '0', '-map', 'a', f'{audio_dir}{audio_file}'])

if __name__ == "__main__":
    main()