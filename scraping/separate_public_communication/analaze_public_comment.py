
import datetime
import json
import logging
import os
import re
import sys
import traceback
import pprint
import collections


import get_address
import get_keyword_list
import get_sentence_list as get_sentence_list 
import get_specific_data_from_metadata as get_spe_data
import get_category_list as category

DIRECTORY = 'test'
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

def get_public_comment_summary_page(page_data):

    target_page_set = set()
    for page in page_data:
        for word in page_data[page]["word_list"]:
            if PUBLIC_COMMENT_NUM.search(word['word']):
                target_page_set.add(page)
    return list(target_page_set)

def get_communication_num(page_data):

    for page in page_data:
        for word in page_data[page]["word_list"]:
            clear_word = word['word'].strip()
            if re.search(r'COMMUNICATIONS$', clear_word):
                conma_index = word['word'].find('.')
                return str(romanToInt(word['word'][:conma_index]))

def transform_comment_data_set(comment_data_set):

    for page, comment_data in comment_data_set.items():
        
        if os.path.isfile(comment_data['public_comment_path']):
            with open(comment_data['public_comment_path'], ) as r:
                comment_data['keyword_list'] = get_keyword_list.get_keyword_list(r.read())
                comment_data['address'].extend(get_address.get_address(r.readlines()))
                comment_data['address'].extend(get_address.get_address(comment_data['summary']))
            comment_data['address'].extend(get_spe_data.get_address(comment_data['summary']))
        
        return {
            comment_data['comment_number']: {
                    'summary': comment_data['summary'],
                    'address': comment_data['address'],
                    'keyword_list': comment_data['keyword_list'],
                    'name': get_spe_data.get_name(comment_data['summary']),
                    'topic': get_spe_data.get_topic(comment_data['summary']),
                    'date': comment_data['date'],
                    'category': get_category(comment_data["keyword_list"], comment_data["summary"])
                }
            for page, comment_data in comment_data_set.items() if comment_data['analyze']
        }

def get_category(keyword_list, summary):

    category_list_1 = []
    category_list_1.extend(category.get_category_list(keyword_list))
    category_list_1.extend(category.get_category_from_summary(summary))
    category_list = list(set(category_list_1))
    if len(category_list) > 1 and 'Miscellaneous' in category_list:
        category_list = [ category for category in category_list if category != 'Miscellaneous']
    return category_list

def log_traceback(ex, ex_traceback, pdf_file):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex_traceback)
    tb_text = ''.join(tb_lines)
    logging.error(pdf_file)
    logging.error(tb_text)

def initialize():

    if not os.path.isdir('each_public_comment_pdf'):
        os.mkdir('each_public_comment_pdf')
    if not os.path.isdir('each_public_comment'):
        os.mkdir('each_public_comment')
    if not os.path.isdir('pdf_text_box'):
        os.mkdir('pdf_text_box')
    if not os.path.isdir('jpg'):
        os.mkdir('jpg')
    if not os.path.isdir('separated_pdf'):
        os.mkdir('separated_pdf')
    if not os.path.isdir('metadata'):
        os.mkdir('metadata')
    if not os.path.isdir('new_metadata'):
        os.mkdir('new_metadata')

def get_category_with_frequency(comment_path):

    noun_word_counter_set = set()
    with open(f'{PUBLIC_COMMENT}/{comment_path}.txt') as r:
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

    json_path_list = get_read_file_list(DIRECTORY)

    for i, json_path in enumerate(json_path_list):

        all_comment_data_set = {}
        try:
            print(f"{DIRECTORY}/{json_path}")
            with open(f"{DIRECTORY}/{json_path}") as r:
                comment_data_dict = json.loads(r.read())
                comment_name_list = [ comment_name for comment_name in comment_data_dict ]
                for comment_name, comment_data in comment_data_dict.items():
                    comment_path = comment_name.strip()
                    comment_data['category_with_frequency'] = get_category_with_frequency(comment_path)
                    comment_data['address'].extend(get_address.get_address([comment_data['summary']]))
                    comment_data['address'] = list(set([address.strip() for address in comment_data['address']]))
                all_comment_data_set = {**all_comment_data_set, **comment_data_dict}
            with open(f'new_metadata/{json_path}', 'w') as write:
                write.write(json.dumps(all_comment_data_set))


        except Exception as ex:
            print(f"Fail to analyze {json_path}.txt")
            _, _, ex_traceback = sys.exc_info()
            log_traceback(ex, ex_traceback, json_path)

   # with open(f'all_comment_metadata.json', 'w') as write:
   #     write.write(json.dumps(all_comment_data_set))

if __name__ == '__main__':
    main()
