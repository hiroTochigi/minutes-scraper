
import itertools
import json
import logging
import re
import sys
import traceback

ALIAS = {
    "Drive": "Dr",
    "Square": "Sq",
    "Street": "St",
    "Avenue": "Ave",
    "Road": "Rd"
}

street_name_end_list = ['Drive', 'Lane', 'Row', 'Hill', 'Place', 'Tpke', 'Circle', 'Terrace', 'Exn', 'Boulevard', 'Highway', 'Gardens', 'Park', 'Court', 'Broadway', 'Road', 'Square', 'Center', 'Green', 'Montague', 'Gdns', 'Mews', 'Street', 'Avenue', 'Pkwy', 'Alt', 'Way', 'Exd', 'Dr', 'Sq', 'St', 'Ave', 'Rd']

ADDRESS_PATTERN = re.compile(r'^[0-9]{1,}\s')

def log_traceback(ex, ex_traceback, sentence_list):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex_traceback)
    tb_text = ''.join(tb_lines)
    logging.error(sentence_list)
    logging.error(tb_text)

def get_street_list():

    street_list = []
    with open("env/street_list.json", "r") as r:
        street_list = json.loads(r.read())["street_list"]
    return street_list

def get_street_name_list(street_list):

    street_name_set = set()
    for street in street_list:
        street_element = street.split(" ")
        if len(street_element[0]) == 1:
            street_name_set.add(street_element[1])
        else:
            street_name_set.add(street_element[0])
    street_name_list = sorted(list(street_name_set))
    return street_name_list


def get_street(target_street, street_list):
    return [street for street in street_list if street.find(target_street)>=0]

def get_unique_word_list(sentence_list):
    word_set = set()
    for sentence in sentence_list:
            temp_words = sentence.split(" ")
            temp_words = [
                    word.replace("\r", "").replace("\n", "")
                    for word in temp_words
                    if len(word)
                ]
            if temp_words:
                for word in temp_words:
                    word_set.add(word)
    return list(word_set)

def get_choice_context_list(sentence, street_name_candidate_list, street_candidate_list):

    temp_words = sentence.split(" ")
    target_street_name_list = [
            word for word in temp_words if word in street_name_candidate_list
        ]
    nested_street_list = [
            get_street(street_name, street_candidate_list) for street_name in target_street_name_list
        ]
    choice_list = sorted(list(itertools.chain.from_iterable(nested_street_list)))

    word_list = sentence.split()
    choice_context_list = []
    for index, word in enumerate(word_list):
        for choice in choice_list:
            first_word_choice = choice.split()[0]
            choice_context = ""
            if word == first_word_choice:
                for i in range(4):
                    if index + i < len(word_list):
                        start = index - 1 
                        choice_context = "".join([word + " " for word in word_list[start:start + i + 1]])
                choice_context_list.append(choice_context)
    return choice_context_list

def does_find_street_name(choice_context, choice_list):

    return any([choice_context.find(choice)>-1 for choice in choice_list])

def erase_exact_choice(choice_context_list, choice_list):

    new_choie_context_list = [choice_context for choice_context in choice_context_list if not does_find_street_name(choice_context, choice_list)]
    return new_choie_context_list

def get_street_name_candidate_list(sentence_list, street_name_list):

    unique_word_list = get_unique_word_list(sentence_list)
    street_name_candidate_list = [word for word in unique_word_list if word in street_name_list ]
    return street_name_candidate_list

def get_street_candidate_list(street_name_candidate_list, street_list):

    nested_street_candidate_list = [
            get_street(
                    street_name,
                    street_list
                )
            for street_name in street_name_candidate_list
        ]
    return sorted(list(itertools.chain.from_iterable(nested_street_candidate_list)))

def add_alias(incomplete_street_list):
    street_list = []
    for street in incomplete_street_list:
        prefix = street.split()[-1]
        alias = ALIAS.get(prefix, None) 
        if alias:
            street_list.append(
                    "".join([f"{st} " for st in street.split()[:-1]])
                    + alias
                )
        street_list.append(street)
    return street_list

def crop_address(address):

    if not address:
        return address
    else:
        address_el = address.split()
        address_end = 0
        for index, el in enumerate(address_el):
            address_end = index
            result = re.search(r'\w{1,}', el)
            if not result:
                continue
            span = result.span()
            el = el[span[0]:span[1]]
            address_el[index] = el

            if el.capitalize() in street_name_end_list:
                break

        if len(address_el) > address_end:
            address_end += 1 
        return ''.join([f'{el} ' for el in address_el[:address_end]])[:-1]


def get_address(sentence_list):

    try:
        street_list = get_street_list()
        street_name_list = get_street_name_list(street_list)

        street_list_in_each_sentence = []

        street_name_candidate_list = get_street_name_candidate_list(
                sentence_list,
                street_name_list
            )
        incomplete_street_candidate_list = get_street_candidate_list(
                street_name_candidate_list,
                street_list
            )
        street_candidate_list = add_alias(incomplete_street_candidate_list)
        street_list = add_alias(street_list)

        for sentence in sentence_list:

            word_list = sorted(list(set(sentence.split(" "))))
            choice = [street for street in street_list if sentence.lower().find(street.lower())>-1]

            choice_context_list = get_choice_context_list(
                    sentence,
                    street_name_candidate_list,
                    street_candidate_list
                )
            reminders = erase_exact_choice(list(set(choice_context_list)), choice)
            address_list = [choice_context for choice_context in list(set(choice_context_list)) if not choice_context in reminders and ADDRESS_PATTERN.search(choice_context)]
            address_list = [crop_address(address) for address in address_list]

            street_list_in_each_sentence.extend(address_list)
        return list(set(street_list_in_each_sentence))

    except Exception as ex:
        _, _, ex_traceback = sys.exc_info()
        log_traceback(ex, ex_traceback, sentence_list)
        return [] 