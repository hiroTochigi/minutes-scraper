import re
import os

target = re.compile(r"\d{1,2}.\d{1,2}.[a-z]")
next_page = re.compile(r"^next page$")

def get_read_file_list(input_dir):

    file_name_list = []
    for root, dirs, files in os.walk(f'{input_dir}'):
        file_name_list = [filename for filename in files if filename.find(".txt")>0]
    return file_name_list

def check_bogus_text(file_name):

    with open(file_name) as r:
        text = "".join([el for el in r.readlines()])
        each_page_text_list = [ t.replace('\n', '') for t in target.split(text) if t] 
        return all([next_page.search(each_text) for each_text in each_page_text_list])

def is_bogus_text(text_list):

    text = "".join([el for el in text_list])
    each_page_text_list = [ t.replace('\n', '') for t in target.split(text) if t] 
    return all([next_page.search(each_text) for each_text in each_page_text_list])

def main():

    dir_name = "2020_each_public_comment"
    file_list = get_read_file_list(dir_name)
    for e_file in file_list:
        if check_bogus_text(f"{dir_name}/{e_file}"):
            print(e_file)


if __name__ == '__main__':
    main()

