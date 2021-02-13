
import itertools

def get_street(target_street, street_list):
    return [street for street in street_list if street.find(target_street)>=0]

def get_unique_word_list(file_path):
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
                        choice_context = "".join([word + " " for word in word_list[index:index + i + 1]])
                choice_context_list.append(choice_context)
    return choice_context_list

def does_find_street_name(choice_context, choice_list):

    return any([choice_context.find(choice)>-1 for choice in choice_list])

def erase_exact_choice(choice_context_list, choice_list):

    new_choie_context_list = [choice_context for choice_context in choice_context_list if not does_find_street_name(choice_context, choice_list)]
    return new_choie_context_list

def get_street_name_candidate_list(file_path, street_name_list):

    unique_word_list = get_unique_word_list(file_path)
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

def get_street_list_in_each_sentence(file_path, street_list, street_name_list):

    street_list_in_each_sentence = []
    with open(file_path, "r") as r:

        street_name_candidate_list = get_street_name_candidate_list(
                file_path,
                street_name_list
            )
        street_candidate_list = get_street_candidate_list(
                street_name_candidate_list,
                street_list
            ) 

        for sentence in r.readlines():

            word_list = sorted(list(set(sentence.split(" "))))
            choice = [street for street in street_list if sentence.lower().find(street.lower())>-1]

            choice_context_list = get_choice_context_list(
                    sentence,
                    street_name_candidate_list,
                    street_candidate_list
                )
            reminders = erase_exact_choice(list(set(choice_context_list)), choice)
            picked_list = [choice_context for choice_context in list(set(choice_context_list)) if not choice_context in reminders]

            sentence_and_choice = {
                "sentence": sentence,
                "choice": choice,
                "word_list": word_list,
                "choice_context_list_reminders": reminders,
                "choice_context_list_pick": picked_list
            }
            street_list_in_each_sentence.append(sentence_and_choice)
    return street_list_in_each_sentence