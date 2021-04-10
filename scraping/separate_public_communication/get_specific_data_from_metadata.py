import json
import re

TOPIC_START_WORD = re.compile(r'thanking|expressing|in support of|requesting|regarding')

def cleanup(datum):

    summary = "".join([f'{el} ' for el in datum.split(' ') if len(el)>0])[:-1]
    return summary

def get_street_list():

    with open('street_list.json') as r:
        street_list = json.loads(r.read())
        return street_list['street_list']

def get_topic(summary):

    summary = cleanup(summary)
    if TOPIC_START_WORD.search(summary):
        start = TOPIC_START_WORD.search(summary).span()[1] + 1
        return summary[start:]
    else:
        return summary
        pass

def is_street_name(sentence):

    return any([ sentence.lower().find(street.lower()) > -1 for street in STREET_LIST ])

def get_address(summary):

    summary = cleanup(summary)
    all_sentences = summary.split(',')
    street = ''
    if len(all_sentences) > 1 and not TOPIC_START_WORD.search(all_sentences[1]):
        for index, sentence in enumerate(all_sentences):
            if index > 0 and not TOPIC_START_WORD.search(sentence) and is_street_name(sentence):
                street += sentence
    if len(street) > 0:
        return [street]
    else:
        return []

def get_name(summary):

    summary = cleanup(summary)
    name = ''
    all_sentences = summary.split(',')
    name_contain_sentence = all_sentences[0]
    if name_contain_sentence.find('from') > -1:
        start = name_contain_sentence.find('from') + 5
        name = name_contain_sentence[start:]
        if len(all_sentences) > 1 and not TOPIC_START_WORD.search(all_sentences[1]):
            for index, sentence in enumerate(all_sentences):
                if TOPIC_START_WORD.search(sentence):
                    break
                if index > 0 and not TOPIC_START_WORD.search(sentence) and not is_street_name(sentence):
                    #print(sentence)
                    name += sentence
        return name
    else:
        if name_contain_sentence.lower().find('sundry') > -1:
            return 'Sundry communications'
        elif name_contain_sentence.lower().find('anonymous') > -1:
            return 'Anonymous'
        else:
            print(name_contain_sentence)
            return 'Unknown'

STREET_LIST = get_street_list()

def main():

    with open('all_comment_metadata.json', 'r') as r:
        data = json.loads(r.read())
        keys = [key for key in data]
        with open('all_comment_metadata.txt', 'w') as w:
            for number, datum in data.items():
                summary = "".join([f'{el} ' for el in datum["summary"].split(' ') if len(el)>0])[:-1]
                w.write(f'{number}:\n   topic: {get_topic(summary)}\n   name: {get_name(summary)}\n   address: {get_address(summary)}\n\n')
                #get_topic(summary)
                #get_name(summary)
                #get_address(summary)