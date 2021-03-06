
import common_process
import re
import collections

def get_region_contain_sentences(
        read_file,
        write_file,
        input_dir,
        output_dir,
        street_list,
        street_name_list,
        _ 
    ):

    word_set = set()
    word_list_list = []
    with open(f'{input_dir}/{read_file}', "r") as r:
        text = r.readlines()
        for sentence in text:
            if not re.match(r'[0-9]{1,2}', sentence):
                temp_words = sentence.split(" ")
                temp_words = [word.replace("\r", "").replace("\n", "") for word in temp_words if len(word)]
                if len(temp_words) == 1 or not temp_words[-1]:
                    temp_words = temp_words[:-1]
                if temp_words:
                    for word in temp_words:
                        word_set.add(word)
                    word_list_list.extend(temp_words)
    word_list = collections.Counter(word_list_list)
    #word_list = list(word_set)
    print(read_file)
    common_word_list = word_list.most_common(200)
    for word in common_word_list:
        print(word)
    print()

def main():

    common_process.process_files(
        function=get_region_contain_sentences,
        output_prefix="stat_region",
        input_prefix="texted-pdf",
        input_dir_part="texted-pdf",
        output_dir_part="stat_region",
    )

if __name__ == "__main__":
    main()