import os
import re

from io import StringIO

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

def get_read_file_list(input_dir):

    file_name_list = []
    for root, dirs, files in os.walk(f'{input_dir}'):
        file_name_list = [filename for filename in files if filename.find(".pdf")>0]
    return file_name_list

pdf_file = get_read_file_list('test')
print(pdf_file)


def convert_pdf_to_xml(path):
    '''get all pdf data as xml file format'''
    output = StringIO()
    with open(path, 'rb') as pdf_file:
        extract_text_to_fp(pdf_file, output, laparams=LAParams(), output_type='xml', codec=None)
    xml = output.getvalue()
    file1 = open('allxml.txt', 'w')
    file1.write(xml)
    file1.close()
    print(xml)
    return xml

convert_pdf_to_xml(f'test/{pdf_file[0]}')