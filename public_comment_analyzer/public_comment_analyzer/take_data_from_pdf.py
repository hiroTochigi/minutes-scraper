import os
import re

from io import StringIO

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

def convert_pdf_to_xml(path):
    '''get all pdf data as xml file format'''
    output = StringIO()
    with open(path, 'rb') as pdf_file:
        extract_text_to_fp(pdf_file, output, laparams=LAParams(), output_type='xml', codec=None)
    xml = output.getvalue()
    return xml
