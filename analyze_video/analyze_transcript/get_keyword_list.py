from nltk import pos_tag
import nltk
from nltk import RegexpParser
import collections
from nltk.stem.porter import *

import os

stemmer = PorterStemmer()

def clean_text(text):
    text = text.replace('next page', '')
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace('“', '')
    text = text.replace('”', '')
    text = text.replace('/n', ' ')
    text = text.replace('.', ' ')
    text = text.replace(',', ' ')
    text = text.lower()
    return text

def get_noun_counter(text) -> collections.Counter: 

    text = text.split()
    tokens_tag = pos_tag(text)
    patterns= """mychunk:{<JJ.?>*<NN.?.?>*}"""
    chunker = RegexpParser(patterns)
    output = chunker.parse(tokens_tag)

    noun_list = []
    compound_noun_list = []
    for n in output:
        if isinstance(n, nltk.tree.Tree):
            n = str(n)
            part_of_speech = [el.split('/')[1]for el in n.split()[1:]]
            if any([el.find('NN')>-1 for el in part_of_speech]):
                noun = [
                        stemmer.stem(el.split('/')[0])
                        if el.split('/')[1] == 'NNS' or el.split('/')[1] == 'NNPS' 
                        else el.split('/')[0] 
                        for el in n.split()[1:]
                    ]
                compound_noun_list.append(''.join([ f'{n} ' for n in noun ])[:-1])
                noun_list.extend(noun)

    noun_list = [ noun for noun in noun_list if len(noun) > 1]

    return collections.Counter(noun_list), compound_noun_list

def is_target_noun(compound_noun, common_word):

    return(
        any([ len(noun) <= len(common_word) + 2 and noun.find(common_word)>-1 for noun in compound_noun.split() ])
        or
        any([ len(noun) <= len(common_word) + 2 and noun.find(common_word)>-1 for noun in compound_noun.split('-') ])
    )

def _get_keyword_list(common_word_list, compound_noun_list):

    compound_word_dict = {}
    for common_word in common_word_list:
        compound_word_dict[common_word] = []
        for compound_noun in compound_noun_list:
            if is_target_noun(compound_noun, common_word):
                compound_word_dict[common_word].append(compound_noun)
    return compound_word_dict

def print_keyword_list(keyword_list):

    for common_word, compound_noun_list in keyword_list.items():
        print(common_word)
        for compound_noun in compound_noun_list:
            print(compound_noun)
        print()

def get_keyword_list(raw_text):
        text = clean_text(raw_text)
        noun_counter, compound_noun_list = get_noun_counter(text)
        common_word_list = [
                common_word[0] for common_word in noun_counter.most_common(100)
            ]
        keyword_list = _get_keyword_list(common_word_list, compound_noun_list)
        return keyword_list

def main():

    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            with open(f"{root}/{name}") as r:
                keyword_list = get_keyword_list(r.read())
                print_keyword_list(keyword_list)
        

if __name__ == '__main__':
    main()


        