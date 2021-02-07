
from copy import deepcopy
import json
import os
import re

from common_process import process_files
from get_street_list_in_each_sentence import get_street_list_in_each_sentence 

class SaveData:
    dataset = {}
    
    @classmethod
    def save_data(cls, file_name, data):
        cls.dataset[file_name] = data
        with open("classify_region.json", "w") as w:
            w.write(json.dumps(cls.dataset[file_name]))
    
    @classmethod
    def load_data(cls):
        with open("classify_region.json", "r") as r:
            cls.dataset = json.loads(r.read())


def print_answer(answer):
    if len(answer) == 0:
       pass
    else: 
        print(f"you choice {answer}")

def get_choice_num(choice_list):
    if len(choice_list) == 0:
        return f"No more choice\n"
    if len(choice_list) == 1:
        return f"Only one choice\n"
    else:
        return f"Enter number: 0-{len(choice_list)-1}\n"

def evaluate_choices(sentence, answer):
    print(f"answer:{answer}")
    print(sentence["choice"])
    print([each_choice in answer for each_choice in sentence["choice"]])
    print(all([each_choice in answer for each_choice in sentence["choice"]]))
    return all([each_choice in answer for each_choice in sentence["choice"]])

def get_region_contain_sentences(
        read_file,
        write_file,
        input_dir,
        output_dir,
        street_list,
        street_name_list
    ):

    street_list_in_each_sentence = get_street_list_in_each_sentence(
            file_path=f'{input_dir}/{read_file}',
            street_list=street_list,
            street_name_list=street_name_list
        )
    answer_list = []
    for sentence in street_list_in_each_sentence:
        print(sentence["sentence"])
        choice = sentence["choice"]
        answer = []
        val = 0
        if not evaluate_choices(sentence, answer_list):
            while val != "n":
                
                print_answer(answer)
                [ print(f"{index}:{choice}") for index, choice in enumerate(choice)]
                val = input(
                        f"{get_choice_num(choice)}" 
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
            answer_list.extend(answer)
    SaveData.save_data(read_file, answer_list)

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