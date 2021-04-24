
def get_word_block(data):

    BBOX_KEYWORD = '<textline bbox="'
    START_BOX = len(BBOX_KEYWORD)

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
                ordered_word_set_list = sorted(word_set_list, key=lambda word_box: word_box['top'], reverse=True)
                word_set_list_set[page] = {'word_list': ordered_word_set_list, 'page_data': page_data}
                word_set_list = []
            page = datum[datum.find('id')+4:datum.find('bbox')-2]
            bbox_set = datum[datum.find('bbox="')+7:datum.find('" rotate')].split(',')
            page_data = {
                "right": float(bbox_set[2]),
                "buttom": float(bbox_set[3]),
            }
        elif datum.find(BBOX_KEYWORD)>-1:
            start = True
            bbox_set = datum[START_BOX:-2].split(',')
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
    
    ordered_word_set_list = sorted(word_set_list, key=lambda word_box: word_box['top'], reverse=True)
    word_set_list_set[page] = {'word_list': ordered_word_set_list, 'page_data': page_data}
        
    return word_set_list_set