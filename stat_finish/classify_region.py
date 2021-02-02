
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
        street_name_list
    ):

    word_set = set()
    word_list_list = []
    with open(f'{input_dir}/{read_file}', "r") as r:
        text = r.readlines()
        for sentence in text:
           print(sentence) 

    """
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
    """

process_files(
    function=get_region_contain_sentences,
    output_prefix="stat_region",
    input_prefix="region",
    input_dir_part="test",
    output_dir_part="stat_region"
)