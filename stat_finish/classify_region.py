
from copy import deepcopy
import json
import os
import re

from common_process import process_files

def print_answer(answer):
    if len(answer) == 0:
       pass
    else: 
        print(f"you choice {answer}")

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
                temp_words = sentence.split(" ")
                temp_words = [word.replace("\r", "").replace("\n", "") for word in temp_words if len(word)]
                if temp_words:
                    for word in temp_words:
                        word_set.add(word)
                    word_list_list.append(temp_words)
                    
        word_list = list(word_set)
        street_name_candidate_list = [word for word in word_list if word in street_name_list ]

        street_list_in_each_sentence = []
        for sentence in text:
            temp_words = sentence.split(" ")
            street_list = [word for word in temp_words if word in street_name_candidate_list]
            sentence_and_choice = {
                "sentence":sentence,
                "choice":street_list
            }
            street_list_in_each_sentence.append(sentence_and_choice)
    for sentence in street_list_in_each_sentence:
        print(sentence["sentence"])
        choice = sentence["choice"]
        answer = []
        val = 0
        while val != "n":
            
            print_answer(answer)
            [ print(f"{index}:{choice}") for index, choice in enumerate(choice)]
            val = input(
                    f"Enter number: 0-{len(choice)-1}\n" 
                    "next sentence for n\n"
                    "repeat sentence for r\n" 
                    "undo choice for u\n"
                )
            if val.isnumeric():
                val = int(val)
                if val >= len(choice):
                    print("Wrong value")
                else:
                    answer.append(choice.pop(val))
            elif val == "r":
                print(sentence["sentence"])
            elif val == "u":
                if len(answer) > 0:
                    choice.append(answer.pop())
                else:
                    print("No answer")


            print()

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