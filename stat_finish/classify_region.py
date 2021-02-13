
from copy import deepcopy
import json
import os
import re
import traceback
import itertools

import common_process
import get_street_list_in_each_sentence 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class JsonIOControler:
    
    dataset = {}
    exclusive_list = []
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
        if os.stat("classify_region.json").st_size == 0:
            self.dataset = {}
        else:
            with open("classify_region.json", "r") as r:
                self.dataset = json.loads(r.read())
            if self.dataset.keys():
                self.exclusive_list = list(self.dataset.keys())
            else:
                self.exclusive_list = []

    def get_exclusive_list(self):
        return self.exclusive_list

    def add_street_to_street_list(self, street):
        street_list = []

        with open("street_list.json", "r") as r:
            street_list_json = json.loads(r.read())
            street_list = street_list_json["street_list"]
            street_list.append(street)

        with open("street_list.json", "w") as w:
            new_street_list_json = {}
            new_street_list_json["street_list"] = street_list
            w.write(json.dumps(new_street_list_json))

def get_region_contain_sentences(
        read_file,
        write_file,
        input_dir,
        output_dir,
        street_list,
        street_name_list,
        json_io_cont
    ):

    exclusive_input = json_io_cont.get_exclusive_list()
    if not read_file in exclusive_input:
        
        command = ""
        while command != "n":

            street_list = common_process.get_street_list()
            street_name_list = common_process.get_street_name_list(street_list)

            street_list_in_each_sentence = get_street_list_in_each_sentence.get_street_list_in_each_sentence(
                    file_path=f'{input_dir}/{read_file}',
                    street_list=street_list,
                    street_name_list=street_name_list
                )
                
            answer_list = []
            for sentence in street_list_in_each_sentence:
                answer_list.extend(sentence["choice"])
                print("--------------------------------------------")
                print("sentence")
                print(sentence["sentence"])
                print("Pick up")
                for choice_context in sentence["choice_context_list_pick"]:
                    print(f"{bcolors.HEADER}{choice_context}{bcolors.ENDC}")
                print("Reminders")
                for choice_context in sentence["choice_context_list_reminders"]:
                    print(f"{bcolors.OKBLUE}{choice_context}{bcolors.ENDC}")
                print("--------------------------------------------")
                print()
            
            answer_list = sorted(list(set(answer_list)))
            for answer in answer_list:
                print(answer)

            print()
            command = input(
                    "       n: Next file\n"
                    "       a: Add street name to street_list and parse again\n"
                    "       e: Edit street name\n"
                    "any keys: Parse again the same file\n"
                )
            
            if command == "a":
                street = input("street name:")
                json_io_cont.add_street_to_street_list(street)
            elif command == "e":
                edit_command = ""
                while not edit_command in ["s", "r"]:

                    edit_command = input(
                    "       d: Delete street name\n"
                    "       s: Save and go to next file\n"
                    "       r: Discard edit and parse again\n"
                    )
                    if edit_command == "d":
                        delete_command = ""
                        while delete_command != "s":
                            for index, answer in enumerate(answer_list):
                                print(f"{index}: {answer}")
                            delete_command = input(
                                f"Enter number [0-{len(answer)-1}]: delete corresponding item\n"
                                f"s: Save and go to edit mode\n"
                            )
                            if delete_command.isnumeric():
                                index = int(delete_command)
                                if index >= len(answer_list):
                                    print(f"Invalid number\n Enter number [0-{len(answer)-1}]")
                                else:
                                    answer_list.remove(answer_list[index])
                    elif edit_command == "s":
                        command = "n"
        json_io_cont.save_data(read_file, answer_list)
        print(chr(27) + "[2J")
        
def main():
    try:
        json_io_cont = JsonIOControler()
        json_io_cont.load_data()

        common_process.process_files(
            function=get_region_contain_sentences,
            output_prefix="stat_region",
            input_prefix="region",
            input_dir_part="region",
            output_dir_part="stat_region",
            save_data_conf=json_io_cont
        )

        json_io_cont.save_file()
    except KeyboardInterrupt:
        pass
        json_io_cont.save_file()
    except Exception as ex:
        json_io_cont.save_file()
        tb_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
        tb_text = ''.join(tb_lines)
        print(tb_text)

if __name__ == "__main__":
    main()
