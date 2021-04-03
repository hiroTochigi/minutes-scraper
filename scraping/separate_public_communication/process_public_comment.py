
import copy
import os
import re

from typing import Union

import take_data_from_pdf as tdfp
import process
import get_address

UNUSED_WORD_REGEX = re.compile(r'Packet Pg\.|\d\.\d\.a')

pdf_file = 'COM 662 #2020 .pdf'
abs_pdf_path = f'{os.getcwd()}/{pdf_file}'
data = tdfp.convert_pdf_to_xml(abs_pdf_path)
page_data = process.get_word_block(data)

EMAIL_KEYWORD = ['From:', 'Sent:', 'To:', 'Subject:']

def cut_unused_word(old_page_data):

    page_data = copy.deepcopy(old_page_data)
    for page, data in page_data.items():
        data['word_list'] = [word for word in data['word_list'] if len(word['word'])>1 and not UNUSED_WORD_REGEX.search(word['word'])]
    return page_data

def grouped_by_height(page_data):

    for page, data in page_data.items():
        for index, word_box in enumerate(data['word_list']):
            if index == 0:
                word_box['diff'] = word_box['top'] - data['word_list'][index+1]['top']
            elif index == len(data['word_list']) - 1:
                word_box['diff'] =  None
            else:
                word_box['diff'] = word_box['top'] -  data['word_list'][index+1]['top']
    return page_data
        
def add_sentence_group_id(page_data):

    group_criterion = (0, 15)
    for page, data in page_data.items():
        sentence_id = 0
        for index, word_box in enumerate(data['word_list']):
            if word_box['diff'] == None:
                word_box['sentence_id'] = sentence_id
                continue
            word_box['sentence_id'] = sentence_id
            if group_criterion[0] <= word_box['diff'] <= group_criterion[1]:
                continue
            else:
                sentence_id = sentence_id + 1
        sentence_id = 0
    return page_data

def get_sentence_grouped(page_data):

    new_page_data = {}
    for page, data in page_data.items():
        new_page_data[page] = {}
        for index, word_box in enumerate(data['word_list']):
            sentence_id = word_box['sentence_id']
            if not sentence_id in new_page_data[page]:
                new_page_data[page][sentence_id] = []
                new_page_data[page][sentence_id].append(word_box)
            else:
                new_page_data[page][sentence_id].append(word_box)
    return new_page_data

def get_sentence_grouped_by_top(sentence_list):

    sentence_grouped_by_top = {}
    for sentence in sentence_list:
        top = sentence['top']
        if top in sentence_grouped_by_top:
            sentence_grouped_by_top[top].append(sentence['word'])
        else:
            sentence_grouped_by_top[top] = []
            sentence_grouped_by_top[top].append(sentence['word'])
    return sentence_grouped_by_top 

def get_clean_sentence_grouped(grouped_sentence):
    
    new_page_data = {}
    for page, data in grouped_sentence.items():
        new_page_data[page] = {}
        for sentence_id, sentence_list in data.items():
            new_page_data[page][sentence_id] = {
                'sentence': "".join([ f'{sentence["word"]} ' for sentence in sentence_list ]).strip(),
                'diff': sentence_list[len(sentence_list)-1]['diff']
                }
    return new_page_data

def is_email(sentence_list: dict) -> Union[int, None] :

    for sentence_id, sentence in sentence_list['1'].items():
        find_num = 0
        for keyword in EMAIL_KEYWORD:
            if sentence['sentence'].find(keyword) > -1:
                find_num += 1
        if find_num == len(EMAIL_KEYWORD):
            return sentence_id
    return None

def is_email_header(sentence):

    find_num = 0
    for keyword in EMAIL_KEYWORD:
        if sentence['sentence'].find(keyword) > -1:
            find_num += 1
    if find_num == len(EMAIL_KEYWORD):
        return True
    return False

def start_index(sentence, id):

    return sentence.find(EMAIL_KEYWORD[id]) + len(EMAIL_KEYWORD[id])

def end_index(sentence, id):
    
    return sentence.find(EMAIL_KEYWORD[id])

def get_email_header_data(sentence):

    return {
        EMAIL_KEYWORD[0]: sentence[start_index(sentence, 0):end_index(sentence, 1)],
        EMAIL_KEYWORD[1]: sentence[start_index(sentence, 1):end_index(sentence, 2)],
        EMAIL_KEYWORD[2]: sentence[start_index(sentence, 2):end_index(sentence, 3)],
        EMAIL_KEYWORD[3]: sentence[start_index(sentence, 3):],
    }

def get_whole_text(clean_sentence_grouped_set):

    whole_text = ""
    for page, sentence_grouped in clean_sentence_grouped_set.items():
        for sentence_id, sentence in sentence_grouped.items():
            if not ((page == '1' and sentence_id == 0) or is_email_header(sentence)):
                whole_text += f"{sentence['sentence']} "
    return whole_text

def get_sentence_list(clean_sentence_grouped_set):

    sentence_list = [] 
    for page, sentence_grouped in clean_sentence_grouped_set.items():
        for sentence_id, sentence in sentence_grouped.items():
            if not ((page == '1' and sentence_id == 0) or is_email_header(sentence)):
                sentence_list.append(sentence['sentence'])
    return sentence_list

new_page_data = cut_unused_word(page_data)
groupd_by_height_page_data = grouped_by_height(new_page_data)
page_data_with_sentence_id = add_sentence_group_id(groupd_by_height_page_data)
sentence_grouped_set = get_sentence_grouped(page_data_with_sentence_id)
clean_sentence_grouped_set = get_clean_sentence_grouped(sentence_grouped_set)
email_header_id = is_email(clean_sentence_grouped_set)
if not email_header_id is None:

    address_list = [ 
            address for address in 
            get_address.get_address(get_sentence_list(clean_sentence_grouped_set)) if len(address) > 0 
        ]
    print(address_list)
    #for page, sentence_grouped in clean_sentence_grouped_set.items():
    #    for sentence_id, sentence in sentence_grouped.items():
    #        if not ((page == '1' and sentence_id == 0) or is_email_header(sentence)):
    #            print(sentence['sentence'])


#get_email_header_data(clean_sentence_grouped_set['1'][email_header_id]['sentence'])



#for page, data in page_data_with_sentence_id.items():
#    for word in data['word_list']:
#        print(word)
#    print()