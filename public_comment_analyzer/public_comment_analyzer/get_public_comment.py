
import datetime
import json
import logging
import os
import re
import sys
import traceback

from PyPDF2 import PdfFileReader, PdfFileWriter

import get_address
import get_keyword_list
import get_sentence_list as get_sentence_list 
import get_specific_data_from_metadata as get_spe_data
import get_read_file_list as grfl
import process
import take_data_from_pdf as tdfp
import extract_text_by_orc as orc
import get_category_list as category
import separate_pdf_and_ocr as separate
import check_bogus_text as bogus

DATA_DIRECTORY = 'data'
LOG_DIRECTORY = 'logs'
TEMP_DIRECTORY = 'temp'

DOWNLOAD_PDF = 'data/pdf'
INPUT_DIRECTORY = 'data/test'
OUTPUT_DIRECTORY = 'data/new_metadata'
TEXT_PUBLIC_COMMENT  = 'data/each_public_comment'
PDF_PUBLIC_COMMENT  = 'data/each_public_comment_pdf'
EACH_METADATA_DIRECTORY = 'data/each_metadata'
PDF_BOX = 'logs/pdf_text_box'
JPG = 'temp/jpg'
SEPARATED_PDF = 'temp/separated_pdf'
METADATA_DIRECTORY = 'data/metadata'

PUBLIC_COMMENT_NUM = re.compile(r'COM\s\d{1,4}\s#')
PUBLIC_COMMENT_EXPLANATION = re.compile(r'^\d{1,2}\.')

logging.basicConfig(filename='get_public_comment_improve.log')

#extracted_list = [ data[len('public_comment_'):-len('.txt')] for data in grfl.get_read_file_list('public_comment')]

def get_read_file_list(input_dir):

    file_name_list = []
    for root, dirs, files in os.walk(f'{input_dir}'):
        file_name_list = [filename for filename in files if filename.find(".pdf")>0]
    return file_name_list

def get_public_comment_summary_page(page_data):

    target_page_set = set()
    for page in page_data:
        for word in page_data[page]["word_list"]:
            if PUBLIC_COMMENT_NUM.search(word['word']):
                target_page_set.add(page)
    return list(target_page_set)

def romanToInt(s):
      """
      :type s: str
      :rtype: int
      """
      roman = {'I':1,'V':5,'X':10,'IV':4,'IX':9}
      i = 0
      num = 0
      while i < len(s):
         if i+1<len(s) and s[i:i+2] in roman:
            num+=roman[s[i:i+2]]
            i+=2
         else:
            #print(i)
            num+=roman[s[i]]
            i+=1
      return num

def get_communication_num(page_data):

    for page in page_data:
        for word in page_data[page]["word_list"]:
            clear_word = word['word'].strip()
            if re.search(r'COMMUNICATIONS$', clear_word):
                conma_index = word['word'].find('.')
                return str(romanToInt(word['word'][:conma_index]))

def get_index(word):

    index = None
    index = re.findall(r'\d{1,2}\.', word['word'])[0][:-1]
    assert index.isdigit()
    return index

def get_page_list(page_data, table_index):

    page_list = []
    table_index_regex = re.compile(r'{}'.format(table_index))
    for page in page_data:
        for word in page_data[page]["word_list"]:
            if table_index_regex.search(word['word']):
                page_list.append(int(page)-1)
    return page_list

def save_text_box_as_txt(page_data, pdf_file):

    file1 = open(f'{PDF_BOX}/{pdf_file}.txt', 'w')
    for page, word_set_list in page_data.items():
        file1.write(f'{page}\n')
        for word_set in word_set_list:
            if word_set == 'word_list':
                for word_set in word_set_list[word_set]:
                    file1.write(f'{word_set}\n')
                file1.write(f'\n')
    file1.close()

def convert_space_to_underscore(comment_id):

    return ''.join([f'{val}_' for val in comment_id.strip().split(' ')])[:-1]

def transform_comment_data_set(comment_data_set):

    for page, comment_data in comment_data_set.items():
        
        if comment_data['analyze']:
            print(f"Analyze {comment_data['public_comment_path_pdf']}")
            text_comments = get_sentence_list.get_sentence_list(
                process.get_word_block(
                        tdfp.convert_pdf_to_xml(comment_data['public_comment_path_pdf'])
                    )
                )

            comment_data['keyword_list'] = {}
            comment_data['address'] = []
            if text_comments and not bogus.is_bogus_text(text_comments):
                with open(f"{comment_data['public_comment_path']}", 'w') as w:
                    for comment in text_comments:
                        w.write(comment)
            else:
                page_num = 0
                with open(comment_data['public_comment_path_pdf'], 'rb') as infile:
                    reader = PdfFileReader(infile)
                    page_num = reader.getNumPages()
                if page_num <= 50:
                    orc.extract_text_by_orc(
                            comment_data['public_comment_path_pdf'],
                            f"{comment_data['public_comment_path']}"
                        )
                elif page_num > 50:
                    separate.separate_pdf_and_ocr(
                            comment_data['public_comment_path_pdf'],
                            f"{comment_data['public_comment_path']}"
                    )
            print("Extract keywords")
            if os.path.isfile(f"{comment_data['public_comment_path']}"):
                with open(f"{comment_data['public_comment_path']}" ) as r:
                    comment_data['keyword_list'] = get_keyword_list.get_keyword_list(r.read())
                    comment_data['address'].extend(get_address.get_address(r.readlines()))
                comment_data['address'].extend(get_spe_data.get_address(comment_data['summary']))
        else:
            print(f"System cannot find {comment_data['public_comment_path_pdf']}")
        
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

def get_military_date(pdf_file):

    start = pdf_file.find(', ') + 2
    end = re.search(r'\d, \d{4}', pdf_file).end()

    year =  pdf_file[start:end].replace(',', '').split()[2]

    day =  int(pdf_file[start:end].replace(',', '').split()[1])
    day = '0' + str(day) if day < 10 else str(day)

    month = pdf_file[start:end].replace(',', '').split()[0]
    month = datetime.datetime.strptime(month, "%B").month
    month = '0' + str(month) if month < 10 else str(month)

    military_date = int(f'{year}{month}{day}')
    return military_date

def log_traceback(ex, ex_traceback, pdf_file):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex_traceback)
    tb_text = ''.join(tb_lines)
    logging.error(pdf_file)
    logging.error(tb_text)

def is_pubic_comment_sumary(word):
    return(
        PUBLIC_COMMENT_EXPLANATION.search(word['word']) 
        and 
        word['word'].lower().find('communication')>-1
    )

def initialize():

    all_dir = [
    DATA_DIRECTORY,
    LOG_DIRECTORY,
    TEMP_DIRECTORY,
    DOWNLOAD_PDF,
    INPUT_DIRECTORY,
    OUTPUT_DIRECTORY,
    TEXT_PUBLIC_COMMENT,
    PDF_PUBLIC_COMMENT,
    EACH_METADATA_DIRECTORY,
    METADATA_DIRECTORY,
    PDF_BOX,
    JPG,
    SEPARATED_PDF]

    for each_dir in all_dir:
        if not os.path.isdir(each_dir):
            os.mkdir(each_dir)

    #if not os.path.isdir('each_public_comment_pdf'):
    #    os.mkdir('each_public_comment_pdf')
    #if not os.path.isdir('each_public_comment'):
    #    os.mkdir('each_public_comment')
    #if not os.path.isdir('pdf_text_box'):
    #    os.mkdir('pdf_text_box')
    #if not os.path.isdir('jpg'):
    #    os.mkdir('jpg')
    #if not os.path.isdir('separated_pdf'):
    #    os.mkdir('separated_pdf')
    #if not os.path.isdir('metadata'):
    #    os.mkdir('metadata')

def are_same_year(comment_number, pdf_date):

    comment_year = re.search(r'#20\d{2}', comment_number).group(0)[1:]
    assert comment_year.isdigit()
    comment_year = int(comment_year)
    pdf_year = int(pdf_date/10000)
    return comment_year == pdf_year

def main():

    initialize()

    pdf_file_list = get_read_file_list(DOWNLOAD_PDF)
    all_comment_data_set = {}

    for i, pdf_file in enumerate(pdf_file_list):

        print(f"Process {pdf_file}")
        try:
            date = get_military_date(pdf_file)

            print(f"Analyze {pdf_file}")
            abs_pdf_path = f'{os.getcwd()}/{DOWNLOAD_PDF}/{pdf_file}'
            data = tdfp.convert_pdf_to_xml(abs_pdf_path)
            page_data = process.get_word_block(data)

            print('Extract COM numbers')
            public_comment_summary_page_list = get_public_comment_summary_page(page_data)
            communication_number = get_communication_num(page_data)

            print('Analyze summary pages')
            comment_data_set = {}
            index = ''
            for page in public_comment_summary_page_list:
                scraping_start = False
                try:
                    for word in page_data[page]['word_list']:

                        if is_pubic_comment_sumary(word):
                            index = get_index(word)

                            comment_data_set[index] = {
                                'comment_number': None,
                                'summary': word['word'],
                                'page_list': get_page_list(
                                        page_data,
                                        f'{communication_number}\.{index}\.[a-z]'
                                    ),
                                'public_comment_path': '',
                                'public_comment_path_pdf': '',
                                'date': date,
                                'analyze': None,
                            }

                            scraping_start = True

                        elif PUBLIC_COMMENT_NUM.search(word['word']):
                            assert not comment_data_set[index]['comment_number']
                            comment_data_set[index]['comment_number'] = word['word']
                            if are_same_year(
                                    comment_data_set[index]['comment_number'],
                                    comment_data_set[index]['date']
                                ):
                                comment_data_set[index]['summary'] = comment_data_set[index]['summary'].strip()
                                comment_data_set[index]['public_comment_path_pdf'] = (
                                    f'{PDF_PUBLIC_COMMENT}/{comment_data_set[index]["comment_number"].strip()}.pdf')
                                comment_data_set[index]['public_comment_path'] = (
                                    f'{TEXT_PUBLIC_COMMENT}/{comment_data_set[index]["comment_number"].strip()}.txt')
                            else:
                                del comment_data_set[index]
                            index = ''
                            scraping_start = False
                        
                        elif scraping_start:
                            comment_data_set[index]['summary'] += f" {word['word']}"

                except Exception as ex:
                    _, _, ex_traceback = sys.exc_info()
                    logging.error(f"{pdf_file} at {page}")
                    log_traceback(ex, ex_traceback, pdf_file)
                    save_text_box_as_txt(page_data, pdf_file)
                    index = ''
                    scraping_start = False

            with open(abs_pdf_path, 'rb') as infile:

                print('Extract each public comment pdf')
                for index, comment_data  in comment_data_set.items():

                    reader = PdfFileReader(infile)
                    writer = PdfFileWriter()
                    for page in comment_data['page_list']:
                        writer.addPage(reader.getPage(page))

                    with open(comment_data['public_comment_path_pdf'], 'wb') as outfile:
                        writer.write(outfile)
                    
                    file_size = os.path.getsize(comment_data['public_comment_path_pdf'])
                    if file_size < 1000:
                        comment_data['analyze'] = False
                    else:
                        comment_data['analyze'] = True 

            print('Make metadata')
            comment_data_set = transform_comment_data_set(comment_data_set)
            all_comment_data_set = {**all_comment_data_set, **comment_data_set}
            with open(f'{EACH_METADATA_DIRECTORY}/{pdf_file}.json', 'w') as write:
                write.write(json.dumps(comment_data_set))


        except Exception as ex:
            print(f"Fail to analyze {pdf_file}")
            _, _, ex_traceback = sys.exc_info()
            log_traceback(ex, ex_traceback, pdf_file)
            save_text_box_as_txt(page_data, pdf_file)

    with open(f'{METADATA_DIRECTORY}/all_comment_metadata.json', 'w') as write:
        write.write(json.dumps(all_comment_data_set))

if __name__ == '__main__':
    main()

    #data = tdfp.convert_pdf_to_xml(abs_pdf_path)
#
    #file1 = open(f'{DIRECTORY}/{txt_file}.json', 'w')
    #word_set_list_set = process.get_word_block(data)
    #file1.write(json.dumps(word_set_list_set))
    #file1.close()


    #for page, word_set_list in word_set_list_set.items():
    #    file1.write(f'{page}\n')
    #    for word_set in word_set_list:
    #        if word_set == 'word_list':
    #            for word_set in word_set_list[word_set]:
    #                file1.write(f'{word_set}\n')
    #            file1.write(f'\n')
    #file1.close()
                    


