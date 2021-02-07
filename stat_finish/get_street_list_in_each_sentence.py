
import itertools

def get_street(target_street, street_list):
    return [street for street in street_list if street.find(target_street)>=0]

def get_word_list(file_path):
    word_set = set()
    with open(file_path, "r") as r:
        text = r.readlines()
        for sentence in text:
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

def narrow_choice(sentence, choice):
    print(choice)
    print(sentence)

    
def get_street_list_in_each_sentence(file_path, street_list, street_name_list):

    word_list = get_word_list(file_path)
    street_name_candidate_list = [word for word in word_list if word in street_name_list ]

    nested_street_candidate_list = [
            get_street(
                    street_name,
                    street_list
                )
            for street_name in street_name_candidate_list
        ]

    street_candidate_list = list(itertools.chain.from_iterable(nested_street_candidate_list))
    street_candidate_list.sort()

    street_list_in_each_sentence = []
    with open(file_path, "r") as r:
        text = r.readlines()
        for sentence in text:
            temp_words = sentence.split(" ")
            target_street_name_list = [
                    word for word in temp_words if word in street_name_candidate_list
                ]
            nested_street_list = [
                    get_street(street_name, street_candidate_list) for street_name in target_street_name_list
                ]
            choice = list(itertools.chain.from_iterable(nested_street_list))
            choice.sort()

            narrow_choice(sentence, choice)

            sentence_and_choice = {
                "sentence":sentence,
                "choice":choice
            }
            street_list_in_each_sentence.append(sentence_and_choice)
    return street_list_in_each_sentence