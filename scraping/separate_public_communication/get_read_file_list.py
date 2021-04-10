
import os

def get_read_file_list(input_dir):

    file_name_list = []
    for root, dirs, files in os.walk(f'{input_dir}'):
        file_name_list = [filename for filename in files if filename.find(".pdf")>0]
    return file_name_list
