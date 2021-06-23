import io
from itertools import groupby
from itertools import cycle
import math
import os
from pathlib import Path
from sys import stderr
import sys
from time import sleep, perf_counter as timer

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.animation import FuncAnimation
from matplotlib import cm
import matplotlib.pyplot as plt

from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets import make_blobs

from resemblyzer.audio import sampling_rate
from resemblyzer import preprocess_wav, VoiceEncoder

from umap import UMAP

from pydub import AudioSegment

import numpy as np

import mutagen
from mutagen.mp3 import MP3

import soundfile as sf

INPUT_DIR = "/analyze/audio/input/"
OUTPUT_DIR = "/analyze/audio/output/"
PLOT = "/analyze/plot/"
INTERVAL = 1
TIMES = 1000

_default_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
_my_colors = np.array([
    [0, 127, 70],
    [255, 0, 0],
    [255, 217, 38],
    [0, 135, 255],
    [165, 0, 165],
    [255, 167, 255],
    [97, 142, 151],
    [0, 255, 255],
    [255, 96, 38],
    [142, 76, 0],
    [33, 0, 127],
    [0, 0, 0],
    [183, 183, 183],
    [76, 255, 0],
], dtype=np.float) / 255


def get_audio_length(audio_data):

    audio = MP3(audio_data)
    audio_info = audio.info    
    length_in_secs = int(audio_info.length)
    return length_in_secs

def check_or_make_dir(audio_dir):

    if not os.path.isdir(audio_dir):
        os.mkdir(audio_dir)

def return_sound(sound, start):
    f = io.BytesIO()
    sound[start*TIMES:(start+INTERVAL)*TIMES].export(f, format='wav')
    f.seek(0)
    tmp = io.BytesIO(f.read())
    data, source_sr = sf.read(tmp)
    return data

def plot_projections(embeds, speakers, ax=None, colors=None, markers=None, legend=True, 
                     title="", **kwargs):
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 6))
        
    # Compute the 2D projections. You could also project to another number of dimensions (e.g. 
    # for a 3D plot) or use a different different dimensionality reduction like PCA or TSNE.
    reducer = UMAP(**kwargs)
    projs = reducer.fit_transform(embeds)
    
    # Draw the projections
    speakers = np.array(speakers)
    colors = colors or _my_colors
    for i, speaker in enumerate(np.unique(speakers)):
        speaker_projs = projs[speakers == speaker]
        marker = "o" if markers is None else markers[i]
        label = speaker if legend else None
        ax.scatter(*speaker_projs.T, c=[colors[i]], marker=marker, label=label)

    if legend:
        ax.legend(title="Speakers", ncol=2)
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    
    print(projs)
    return projs

def get_min_index(cluster_centers, all_data_set):

    index_list = []
    for center in cluster_centers:
        length_list = [math.sqrt((center[0]-x[0])**2 + (center[1]-x[1])**2) for x in all_data_set]
        min_length = min(length_list)
        min_index = length_list.index(min_length)
        print(all_data_set[min_index])
        print(min_index)
        index_list.append(min_index)
    return sorted(index_list)

"-----------------------------------------------------------------------------------"

def group(L):
    first = last = L[0]
    for n in L[1:]:
        if n - 1 == last: # Part of the group, bump the end
            last = n
        else: # Not part of the group, yield current group and start a new
            yield first, last
            first = last = n
    yield first, last # Yield the last group

def separate_continuous(speaker_wav_dict_list):
    new_dict = {}
    neo_new_dict = []
    for speaker_wav_dict in speaker_wav_dict_list:
        for speaker, wav_list in speaker_wav_dict.items():
            new_dict[speaker] = list(group(wav_list))
    for speaker, wav_list in new_dict.items():
        neo_new_dict.extend( [({'group':wav, 'index':index, 'speaker':speaker}) 
                              for index, wav in enumerate([wav for wav in wav_list if wav[1] - wav[0] >2])])
        
    neo_new_dict = sorted(neo_new_dict, key=lambda key: key['group'][0])
    neo_new_dict = [
        {'group': [i for i in range(el['group'][0],el['group'][1]+1)] , 
         'speaker_index':el['index'], 
         'index': index,
         'speaker':el['speaker'],
         'len':el['group'][1] - el['group'][0]}
         for index, el in enumerate(neo_new_dict)]
    #neo_new_dict = [el for el in neo_new_dict if el['len']>=2]
    return neo_new_dict

def get_speaker_wav_path_dict(speaker_wav_dict_list, wav_fpaths):
    speaker_wav_path_dict = {}
    for speaker_wav_dict in speaker_wav_dict_list:
        file_name = f"{('00'+str(speaker_wav_dict['index']))[-3:]}-"\
                    f"{('0'+str(speaker_wav_dict['speaker']))[-2:]}-"\
                    f"{('00'+str(speaker_wav_dict['speaker_index']))[-3:]}"
        speaker_wav_path_dict[file_name] = [ wav_fpaths[i] for i in speaker_wav_dict['group'] ]
    return speaker_wav_path_dict

def merge_and_save_sound(audio_dir, speaker_wav_path_dict):
    
    merge_sound = AudioSegment.empty()
    for speaker, sound_list in speaker_wav_path_dict.items():
        print(speaker)
        for sound in sound_list:
            print(type(sound))
            merge_sound += sound
        merge_sound.export(f"{OUTPUT_DIR}{audio_dir}{speaker}.mp3", format="mp3")
        merge_sound = AudioSegment.empty()

'-------------------------------------------------------------------------------------------------'

def get_processed_sound(input_audio):

    sound = AudioSegment.from_file(input_audio)
    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(16000)
    return sound

def get_sound_list(sound, sound_length):

    sound_list = [ sound[start*TIMES:(start+INTERVAL)*TIMES ] for start in range(0, sound_length, INTERVAL)]
    return sound_list

def get_sound_feature_matrix(sound_list):

    temp_list = [ np.array(each_sound.get_array_of_samples()).astype(np.float32) for each_sound in sound_list]
    wav_list = [ y / (1 << 8*2 - 1) for y in temp_list ]
    wavs = np.array([ preprocess_wav(wav) for wav in wav_list ])
    return wavs

def get_utterance_embeds(wavs):

    encoder = VoiceEncoder()
    utterance_embeds = np.array(list(map(encoder.embed_utterance, wavs)))
    return utterance_embeds

for root, dirs, files in os.walk(INPUT_DIR):
    for audio_file in files:
        audio_dir = f"{audio_file.split('.')[0]}/"
        check_or_make_dir(f"{OUTPUT_DIR}{audio_dir}")
        check_or_make_dir(f"{PLOT}{audio_dir}")

        input_audio = f"{INPUT_DIR}{audio_file}"

        sound_length = get_audio_length(input_audio)
        sound = get_processed_sound(input_audio)
        sound_list = get_sound_list(sound, sound_length)
        wavs = get_sound_feature_matrix(sound_list)
        speakers = ['audio' for i in range(0, sound_length, INTERVAL)]
        utterance_embeds = get_utterance_embeds(wavs)

        X = plot_projections(utterance_embeds, speakers, title="Embedding projections")
        plt.savefig(f"{PLOT}{audio_dir}plot_1.png")

        bandwidth = estimate_bandwidth(X, quantile=0.05, n_samples=len(speakers))

        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(X)
        labels = ms.labels_
        cluster_centers = ms.cluster_centers_

        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)

        print("number of estimated clusters : %d" % n_clusters_)
                
        index_list = get_min_index(cluster_centers, X)


        plt.figure(1)
        plt.clf()

        colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
        index_list_set = []
        file_list_set = []
        for k, col in zip(range(n_clusters_), colors):
            my_members = labels == k
            print(k)
            print([ index for index, val in enumerate(my_members) if val] )
            file_list_set.append({k: [ index for index, val in enumerate(my_members) if val]})
            index_list_set.extend([ (k, index) for index, val in enumerate(my_members) if val ])
            cluster_center = cluster_centers[k]
            plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
            plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                    markeredgecolor='k', markersize=14)

        print(file_list_set)
        index_list_set = sorted(index_list_set, key=lambda item: item[1])

        plt.title('Estimated number of clusters: %d' % n_clusters_)
        plt.savefig(f"{PLOT}{audio_dir}plot_2.png")

        file_list = separate_continuous(file_list_set)
        speaker_wav_path_dict = get_speaker_wav_path_dict(file_list, sound_list)
        merge_and_save_sound(audio_dir, speaker_wav_path_dict)