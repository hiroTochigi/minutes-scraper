from copy import deepcopy
import json
import os
import re

from common_process import process_files

def get_region_contain_sentences(
        read_file,
        write_file,
        input_dir,
        output_dir,
        street_list,
        street_name_list,
        _ 
    ):

    word_set = set()
    word_list_list = []
    with open(f'{input_dir}/{read_file}', "r") as r:
        text = r.readlines()
        for sentence in text:
            if not re.match(r'[0-9]{1,2}', sentence):
                temp_words = sentence.split(" ")
                temp_words = [word.replace("\r", "").replace("\n", "") for word in temp_words if len(word)]
                if len(temp_words) == 1 or not temp_words[-1]:
                    temp_words = temp_words[:-1]
                if temp_words:
                    for word in temp_words:
                        word_set.add(word)
                    word_list_list.append(temp_words)
    word_list = list(word_set)
    street_name_candidate_list = [word for word in word_list if word in street_name_list ]

    with open(f'{output_dir}/{write_file}', "w") as w:
        for index, word_list in enumerate(word_list_list):
            if any(word in word_list for word in street_name_candidate_list):
                new_word_list = []
                if index == 0:
                    new_word_list = deepcopy(word_list)
                    new_word_list.extend(word_list_list[index+1])
                elif index == len(word_list_list)-1:
                    new_word_list = deepcopy(word_list_list[index-1])
                    new_word_list.extend(word_list)
                else:
                    new_word_list = deepcopy(word_list_list[index-1])
                    new_word_list.extend(word_list)
                    new_word_list.extend(word_list_list[index+1])
                sentence = " ".join(new_word_list).strip()
                if any(street in sentence for street in street_list):
                    w.write(sentence + "\n")

process_files(
    function=get_region_contain_sentences,
    output_prefix="region",
    input_dir_part="texted-pdf",
    output_dir_part="region"
)