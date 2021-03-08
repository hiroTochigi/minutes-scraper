
bbox_keyword = '<textline bbox="'
start_box = len(bbox_keyword)

with open('allxml.txt', 'r') as r:
    data = r.read()
    data = data.split('\n')

    start = False

    word_set = {}
    word_set_list = []
    word_set_list_set = {}

    page = ''
    page_data = {}

    for datum in data:
        if datum.find('page id')>-1:
            if page:
                word_set_list_set[page] = {'word_list': word_set_list, 'page_data': page_data}
                word_set_list = []
            page = datum[datum.find('id')+4:datum.find('bbox')-2]
            bbox_set = datum[datum.find('bbox="')+7:datum.find('" rotate')].split(',')
            page_data = {
                "right": float(bbox_set[2]),
                "buttom": float(bbox_set[3]),
            }
        elif datum.find(bbox_keyword)>-1:
            start = True
            bbox_set = datum[start_box:-2].split(',')
            word_set = {
                "left": float(bbox_set[0]),
                "top": float(bbox_set[1]),
                "right": float(bbox_set[2]),
                "buttom": float(bbox_set[3]),
                "word": []
            }

        elif datum.find('</textline>')>-1:
            start = False
            word_set['word'] = "".join(word_set['word'])
            word_set_list.append(word_set)
            word_set = {}
        if start and datum.find('<text font=')>-1:
            letter_index = datum.find('">') + 2
            word_set['word'].append(datum[letter_index:letter_index+1])


public_comment_list ={} 
for page, info in word_set_list_set.items():
    position_set = set()
    char_list = []
    for word in info['word_list']:
        if len(word['word']) == 1:
            position_set.add(word['right'])
    max_position = max(position_set)
    char_list = [word['word'] for word in info['word_list'] if word['right'] == max_position]
    char_list.reverse()
    sentence = ''.join(char_list)
    if sentence.find('COM')>-1:
        public_comment_list[page] = sentence
        print(f'Page {page}: {sentence}')
            

page_list = [page for page in public_comment_list]
file1 = open('public_comment.txt', 'w')
for page, info in word_set_list_set.items():
    if page in page_list:
        file1.write(f'page: {page}\n')
        file1.write(f'{public_comment_list[page]}\n')
        for word in info['word_list']:
            if len(word['word']) > 1:
                file1.write(word['word']+"\n")
        file1.write('\n')
file1.close()
            
