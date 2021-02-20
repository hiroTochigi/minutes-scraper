from copy import deepcopy
import json
import os
import re

def get_read_file_list():

    file_name_list = []
    for root, dirs, files in os.walk("."):
        file_name_list = [filename for filename in files if filename.find(".txt")>0]
    return file_name_list

def get_street_list():

    street_list = []
    with open("street_list.json", "r") as r:
        street_list = json.loads(r.read())["street_list"]
    return street_list

def get_street_name_list(street_list):

    street_name_set = set()
    for street in street_list:
        street_element = street.split(" ")
        if len(street_element[0]) == 1:
            street_name_set.add(street_element[1])
        else:
            street_name_set.add(street_element[0])
    street_name_list = sorted(list(street_name_set))
    return street_name_list

def get_region_contain_sentences(read_file, write_file, street_list, street_name_list):

    word_set = set()
    word_list_list = []
    with open(read_file, "r") as r:
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

    with open(write_file, "w") as w:
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

file_name_list = get_read_file_list()
output_file_name_list = ["region_"+filename[:-4] for filename in file_name_list]
street_list = get_street_list()
street_name_list = get_street_name_list(street_list)

for index in range(len(file_name_list)):
    get_region_contain_sentences(
            file_name_list[index],
            output_file_name_list[index],
            street_list,
            street_name_list
        )