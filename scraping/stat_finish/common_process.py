from copy import deepcopy
import json
import os
import re

def get_read_file_list(input_dir):

    file_name_list = []
    for root, dirs, files in os.walk(f'{input_dir}'):
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

def get_index_without_prefix(input_prefix):
    if not input_prefix:
        return 0
    return len(input_prefix)

def process_files(
        function,
        output_prefix,
        input_dir_part,
        output_dir_part,
        input_prefix=None,
        save_data_conf=None
    ):
    CWD = os.getcwd()
    input_dir = f"{CWD}/{input_dir_part}"
    output_dir = f"{CWD}/{output_dir_part}"
    start = get_index_without_prefix(input_prefix)
    file_name_list = get_read_file_list(input_dir)
    output_file_name_list = [f"{output_prefix}_{filename[start:-4]}.txt" for filename in file_name_list]
    street_list = get_street_list()
    street_name_list = get_street_name_list(street_list)
    for index in range(len(file_name_list)):
        function(
                file_name_list[index],
                output_file_name_list[index],
                input_dir,
                output_dir,
                street_list,
                street_name_list,
                save_data_conf
            )
