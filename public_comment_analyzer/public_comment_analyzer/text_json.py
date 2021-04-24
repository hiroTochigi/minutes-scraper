import os

import get_read_file_list as grfl

public_comment_dir = 'public_comment'
text_output = 'each_public_comment'

public_comment_list = grfl.get_read_file_list(public_comment_dir)

for public_comment in public_comment_list:

    start = False
    current_com_num = None

    public_comment_set = {}
    
    stat_data = os.stat(f'{public_comment_dir}/{public_comment}')
    if stat_data.st_size: #and public_comment == 'public_comment_MONDAY, DECEMBER 14, 2020  5:30 PM City Council Regular Meeting.pdf.txt':
        
        with open(f'{public_comment_dir}/{public_comment}', 'r') as r:
            all_text = r.read()
            sentence_list = all_text.split('\n')
            for sentence in sentence_list:
                if sentence.find('Attachment:') > -1:
                    start_index = sentence.find('COM')
                    com_num_with_other_data = sentence[start_index:]
                    com_num_with_whitespace = com_num_with_other_data[:com_num_with_other_data.find(':')]
                    if len(com_num_with_whitespace):
                        com_num = "".join(com_num_with_whitespace.split())
                        if not current_com_num or (current_com_num and current_com_num != com_num): 
                            current_com_num = com_num
                            public_comment_set[current_com_num] = [] 
                elif current_com_num and sentence.find('page:') == -1:
                    sentence = sentence.replace('\t\t', ' ')
                    sentence = sentence.replace('\t', ' ')
                    public_comment_set[current_com_num].append(sentence)
        for com, data in public_comment_set.items():
            with open(f'{text_output}/{com}.txt', 'w') as w:
                for datum in data:
                    w.write(datum)
                    w.write('\n')
            
                            

