import json

with open("street_list.txt", "r") as r:
    text_line = r.readlines()
    street_set = set()
    for text in text_line:
        street_el = text.split(" ")
        street_el = " ".join(street_el[:-1]).strip()
        street_set.add(street_el)

street_dict = {"street_list":list(street_set)}
str_street_list = json.dumps(street_dict)

with open("street_list.json", "w") as write:
    write.write(str_street_list)


