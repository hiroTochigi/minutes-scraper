import get_category_list as category
import get_keyword_list as keyword

import os
import collections
import pprint
import json

pp = pprint.PrettyPrinter(indent=2)

def get_category_with_frequency(key_word_list):

    noun_word_counter_set = set()
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


for root, dirs, files in os.walk("../transcript", topdown=False):
    #if len(root) > 2 and root.find("cambridgema")>0:
    if len(root) > 2 :
        file_list = [name for name in files if name.find(".txt")>0]
        file_list = sorted(file_list)
        analyzed_result_dict = {}
        result_name = root.split('/')[-1] + '.json'
        print(result_name)
        for name in file_list:
            with open(f"{root}/{name}") as r:
                keyword_list = keyword.get_keyword_list(r.read())
                result_category = category.get_category_list(keyword_list)
                result_freq = get_category_with_frequency(keyword_list)

                analyzed_result_dict[name] = {
                    "keyword_list": keyword_list,
                    "category": result_category,
                    "frequency": result_freq
                }
                
        pp.pprint(analyzed_result_dict)
        data = json.dumps(analyzed_result_dict)

        result_name = os.path.join('result', root.split('/')[-1] + '.json')
        with open(result_name, "w") as w:
            w.write(data)
