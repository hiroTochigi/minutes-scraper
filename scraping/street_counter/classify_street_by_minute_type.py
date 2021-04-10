import json
import collections
from functools import reduce

month_dict = {
    "06": "JUNE",
    "07": "JULY",
    "03": "MARCH",
    "11": "NOVEMBER",
    "12": "DECEMBER",
    "05": "MAY",
    "04": "APRIL",
    "09": "SEPTEMBER",
    "08": "AUGUST",
    "10": "OCTOBER",
    "01": "JANUARY",
    "02": "FEBRUARY",
}

ALIAS_PREFIX = {
   "Dr": "Drive",
   "Sq": "Square",
   "St": "Street",
   "Ave": "Avenue",
   "Rd": "Road",
   "Streets": "Street"
}

ALIAS_STREET_NAME = {
    "Mass Avenue": "Massachusetts Avenue",
    "Mt. Auburn Street": "Mount Auburn Street",
    "Kennedy Street": "Jfk Street", 
    "First Street": "1st Street",
    "Second Street": "2nd Street",
    "Third Street": "3rd Street",
    "Fourth Street": "4th Street",
    "Fifth Street": "5th Street",
    "Sixth Street": "6th Street",
}

def replace_street_alias(street_name):
    element = street_name.split()
    prefix = element[-1]
    short_street_prefix = [el for el in ALIAS_PREFIX]
    if prefix in short_street_prefix:
        new_street_name = "".join([el + " " for el in element[:-1]]) + ALIAS_PREFIX.get(prefix)
        return new_street_name
    elif street_name in ALIAS_STREET_NAME:
        return ALIAS_STREET_NAME.get(street_name)
    return street_name

def get_conference_street_name_dict(dict_container, conference_name, street_list):
    if not dict_container.get(conference_name, None):
        dict_container[conference_name] = []
        dict_container[conference_name].extend(street_list)
    else:
        dict_container[conference_name].extend(street_list)
    return dict_container

def count_street_name(street_name_list):
    counter_street = collections.Counter(street_name_list)
    street_name_list = sorted(counter_street, key=lambda key: key)
    sorted_counter_street = {k: v for k, v in sorted(counter_street.items(), reverse=True, key=lambda item: item[1])}
    return sorted_counter_street

def get_how_many_times_street_name_discuss(street_list):
    sum_street_qty = reduce(lambda a, b: a + b, [val for key, val in street_list.items()], 0)
    return sum_street_qty

sorted_counter_street = {}
conference_name_street_dict = {}
with open("classify_region.json", "r") as r:
    dataset = json.loads(r.read())
    conference_name = ""
    long_street_list = []
    for data, street_list in dataset.items():
        element = data.split(", ") 
        if len(element)>=3: 
            date = element[1]
            conference_name_with_time = "".join([f'{el}, ' for el in element[2:]])[:-2]
            conference_name = date + " " + conference_name_with_time[conference_name_with_time.find("M")+2:]
        elif len(element)==1:
            sub_elememt = data.split("-")
            month = month_dict.get(sub_elememt[1], None)
            conference_name = "".join([f'{month} '] + [f'{el} ' for el in sub_elememt[2:]])[:-1]
        conference_name = "".join(el + " " for el in conference_name.split()[2:])[:-5]
        conference_name_street_dict = get_conference_street_name_dict(
                conference_name_street_dict,
                conference_name,
                street_list
            )
        long_street_list.extend([replace_street_alias(street_name) for street_name in street_list])

    sorted_counter_street = count_street_name(long_street_list)

    conference_counted_name_street_dict = {
        conference_name: count_street_name(street_name_list) for 
        conference_name, street_name_list in 
        conference_name_street_dict.items()
    }

number_dict = {}
for street_name, num in sorted_counter_street.items():
    if not number_dict.get(num, None):
        number_dict[num] = 1 
    else:
        number_dict[num] += 1

new_dict = [{"name":k, "value":v} for k, v in sorted_counter_street.items() if v > 2]
data = {"name": "street name", "children": new_dict}

#for conference, street_name in conference_counted_name_street_dict.items():
#
#    print(conference)
#    print(street_name)
#    print(f"street_qty: {get_how_many_times_street_name_discuss(street_name)}")

street_data_list =[
    { 
        "name": conference,
        "children": [{"name": street_name, "value": qty} for street_name, qty in street_name_dict.items()]
    }
    for conference, street_name_dict in conference_counted_name_street_dict.items()
]
for street_data in street_data_list:
    print('{')
    for key, val in street_data.items():
        if key == "children":
            print(f"{key}: [" )
            for i, v in enumerate(val):
                if i == len(val) - 1:
                    print(f"{v}")
                else:
                    print(f"{v},")
            print("]")
        else:
            print(f'{key}: "{val}",')
    print('},')


#print(number_dict)

number_dict = {}
for street_name, num in sorted_counter_street.items():
    if not number_dict.get(num, None):
        number_dict[num] = [] 
        number_dict[num].append(street_name)
    else:
        number_dict[num].append(street_name)


#    
#    for street_name in street_name_list:
#        print(street_name)


