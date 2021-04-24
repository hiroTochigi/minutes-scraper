
import datetime
import json
import logging
import os
import re
import sys
import traceback
import pprint
import collections

from pathlib import Path

import get_address
import get_keyword_list
import get_category_list as category

INPUT_DIRECTORY = 'test'
OUTPUT_DIRECTORY = 'new_metadata'
PUBLIC_COMMENT  = 'each_public_comment'

PUBLIC_COMMENT_NUM = re.compile(r'COM\s\d{1,4}\s#')
PUBLIC_COMMENT_EXPLANATION = re.compile(r'^\d{1,2}\.')

logging.basicConfig(filename='analyze.log')
pp = pprint.PrettyPrinter()

def get_read_file_list(input_dir):

    file_name_list = []
    for root, dirs, files in os.walk(f'{input_dir}'):
        file_name_list = [filename for filename in files if filename.find(".json")>0]
    return file_name_list

def log_traceback(ex, ex_traceback, pdf_file):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex_traceback)
    tb_text = ''.join(tb_lines)
    logging.error(pdf_file)
    logging.error(tb_text)

def initialize():

    if not os.path.isdir(OUTPUT_DIRECTORY):
        os.mkdir(OUTPUT_DIRECTORY)

def get_category_with_frequency(comment_path):

    noun_word_counter_set = set()
    with open(Path(f'{PUBLIC_COMMENT}/{comment_path}.txt')) as r:
        key_word_list = get_keyword_list.get_keyword_list(r.read())
        for key_word, noun_list in key_word_list.items():
            for word, num in collections.Counter(noun_list).items():
                noun_word_counter_set.add(f"{word}:{num}")

    noun_word_counter_list = [ 
            (
                {
                    'compound_noun' :noun_word_counter.split(':')[0], 
                    'frequency': int(noun_word_counter.split(':')[1])
                }
            ) 
            for noun_word_counter in noun_word_counter_set 
            if noun_word_counter.split(':')[1].isdigit() 
        ]
    noun_word_counter_list = sorted(
        noun_word_counter_list,
        key=lambda noun_word_counter: noun_word_counter['frequency'],
        reverse=True
        )
    category_list =  category.find_category_frequency_list(noun_word_counter_list)
    return category_list

def main():

    initialize()

    json_path_list = get_read_file_list(INPUT_DIRECTORY)

    for i, json_path in enumerate(json_path_list):

        all_comment_data_set = {}
        try:
            print(Path(f"{INPUT_DIRECTORY}/{json_path}"))
            with open(Path(f"{INPUT_DIRECTORY}/{json_path}")) as r:
                comment_data_dict = json.loads(r.read())
                comment_name_list = [ comment_name for comment_name in comment_data_dict ]
                for comment_name, comment_data in comment_data_dict.items():
                    comment_path = comment_name.strip()
                    comment_data['category_with_frequency'] = get_category_with_frequency(comment_path)
                    comment_data['address'].extend(get_address.get_address([comment_data['summary']]))
                    comment_data['address'] = list(set([address.strip() for address in comment_data['address']]))
                all_comment_data_set = {**all_comment_data_set, **comment_data_dict}
            with open(Path(f'{OUTPUT_DIRECTORY}/{json_path}'), 'w') as write:
                write.write(json.dumps(all_comment_data_set))

        except Exception as ex:
            print(f"Fail to analyze {json_path}.txt")
            _, _, ex_traceback = sys.exc_info()
            log_traceback(ex, ex_traceback, json_path)

if __name__ == '__main__':
    main()
