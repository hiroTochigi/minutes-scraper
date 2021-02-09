
from copy import deepcopy
import json
import os
import re

from common_process import process_files
from get_street_list_in_each_sentence import get_street_list_in_each_sentence 

class SaveData:
    
    dataset = {}
    def __init__(self):
        pass

    def save_data(self, file_name, data):
        self.dataset[f"{file_name}"] = []
        for da in data:
            self.dataset[file_name].append(da)
    
    def save_file(self):
        with open("classify_region.json", "w") as w:
            w.write(json.dumps(self.dataset))
    
    def load_data(self):
        with open("classify_region.json", "r") as r:
            self.dataset = json.loads(r.read())

    def get_save_list(self):
        return list(self.dataset.keys())

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
    return all([each_choice in answer for each_choice in sentence["choice"]])

def get_region_contain_sentences(
        read_file,
        write_file,
        input_dir,
        output_dir,
        street_list,
        street_name_list,
        save_data_cont
    ):

    street_list_in_each_sentence = get_street_list_in_each_sentence(
            file_path=f'{input_dir}/{read_file}',
            street_list=street_list,
            street_name_list=street_name_list
        )
    print(save_data_cont.get_save_list())
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
                        "add answer manually a\n"
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
                elif val == "a":
                    answer.append(input("Enter street name:"))
                    


                print()
            answer_list.extend(answer)
    save_data_cont.save_data(read_file, answer_list)

def main():
    try:
        save_data_cont = SaveData()
        save_data_cont.load_data()
        process_files(
            function=get_region_contain_sentences,
            output_prefix="stat_region",
            input_prefix="region",
            input_dir_part="test",
            output_dir_part="stat_region",
            save_data_conf=save_data_cont
        )
        save_data_cont.save_file()
    except KeyboardInterrupt:
        save_data_cont.save_file()


if __name__ == "__main__":
    main()