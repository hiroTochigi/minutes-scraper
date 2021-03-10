import os
import re
def get_read_file_list(input_dir):

    file_name_list = []
    for root, dirs, files in os.walk(f'{input_dir}'):
        file_name_list = [filename for filename in files if filename.find(".txt")>0]
    return file_name_list

pdf_file = get_read_file_list('test')
print(pdf_file)


with open(f'test/{pdf_file[0]}') as reader:
    data = reader.readlines()
   # print(data)
    all_chars = []
    for datum in data:
        no_next_line = datum.rstrip("\n")
        no_next_line = datum.lstrip()
        if len(no_next_line) == 2:
            all_chars.append(no_next_line[0])
    all_chars.reverse()
    sentences = ''.join(all_chars)

    last = 0
    count = 0
    while last != -1:
        first = sentences.find('Attachment')
        last = sentences.find(')')
        first_sentences = sentences[first:last+1]
        sentences = sentences[last+1:]
        if first < last:
            print(len(sentences))
            print(first_sentences)
            if first_sentences.find('COM')>=0:
                count += 1
    print(count)



