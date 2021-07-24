import copy
import json
import re

CATEGORY_KEYWORD_LIST = {
    'Housing': {
        'lazy': ["tenant", "propert", "evict",  "affordable housing overlay",  "preserv", "transfer fee", "real estate"],
        'restrict': ["home", "homes", "house", "houses", "zone", "zones", "aho"],
        },
    'Local Economy': {
        "lazy": ["restaurant", "business", "local", "organization"],
        "restrict": ["close", "closes", "gym", "gyms"],
        },
    'Real Estate Development': {
        "lazy": ["project", "mass ave", "street", "revit"],
        "restrict": [],
        },
    'Disaster': {
        "lazy": ["disaster", "relief"],
        "restrict": [],
        },
    'Art': {
        "lazy":[],
        "restrict": ["art", "arts"],
        },
    'School': {
        "lazy": ["school", "crls", "ringe", "superintendent", "teach", "learn"], #references cambridge ringe and latin school
        "restrict": [],
        },
    'Bike': {
        "lazy": ["cycl", ],
        "restrict": ['bike', 'bikes', "lane", "lanes"],
        },
    "Transportation": {
        "lazy": ["parking", "traffic", "pedestrian", "sidewalk", ],
        "restrict": ["car", "cars", "park", "parks"],
        },
    "Public Transportation": {
        "lazy": ["transit", "train", "subway", "mbta", "curb cut"],
        "restrict": ["bus", "buses" ],
        },
    "Health": {
        "lazy": ["covid", "transmission", "ventil", 'social distance', "health", "test"],
        "restrict": ["mask", "masks", "sars"],
        },
    "Environment": {
        "lazy": ["natural gas",  "canop", "environ", "vegetation", "animal", "climate", "charles", "vegetation", "green", "solar"],
        "restrict": ["park", "tree", "parks", "trees"],
        },
    "Police": {
        "lazy": ["police", "tear gas", "milit", "surveill", "shotspotter", ],
        "restrict": ["crime", "crimes"],
        },
    "Cannabis": {
        "lazy": ["cannabis", "weed", "cookies"],
        "restrict": [],
        },
    "Municipal Broadband": {
        "lazy": ["broadband", "internet", "online"],
        "restrict": [],
        },
    "City Manager": {
        "lazy": ["city manager", "contract", "plan e", "charter"],
        "restrict": [],
        },
    "Government Administration": {
        "lazy": ["board", "commission", "home rule"],
        "restrict": [],
        },
    "Campaign Finance Reform": {
        "lazy": ["campaign finance reform"],
        "restrict": [],
        },
    "Racism": {
        "lazy": ["racism", "racial"],
        "restrict": [],
        },
    "In Memorium": {
        "lazy": ["r.i.p.", "rip"],
        "restrict": [],
        },
}

CATEGORY_DICT = {
    name: {
        'lazy': value['lazy'],
        'restrict': value['restrict'],
        'frequency': 0,
        'keyword_list': [],
    } for name, value in CATEGORY_KEYWORD_LIST.items()
}

json_file = 'all_comment_metadata.json'

def find_category_frequency_list(word_freq_list):

    category_data_set = copy.deepcopy(CATEGORY_DICT)
    category_list = [category for category in category_data_set]

    for word in word_freq_list:
        for category in category_list:
            for k_type, keyword_list in category_data_set[category].items():
                if k_type == "restrict":
                    for keyword in keyword_list:
                        if any([el == keyword for el in word['compound_noun'].lower().split()]):
                            category_data_set[category]['frequency'] += word['frequency']
                            category_data_set[category]['keyword_list'].append(word['compound_noun'])
                elif k_type == 'lazy':
                    for keyword in keyword_list:
                        if word['compound_noun'].lower().find(keyword)>-1:
                            category_data_set[category]['frequency'] += word['frequency']
                            category_data_set[category]['keyword_list'].append(word['compound_noun'])
    return [ 
            {
                'category': category,
                'frequency': category_data_set[category]['frequency'],
                'keyword_list': category_data_set[category]['keyword_list'] 
            } 
            for category in category_list if category_data_set[category]['frequency'] > 0 
        ]
    #sorted( key=lambda category_data_set: category_data_set[category]['frequency'], reverse=True )

def find_category(word):

    for category, keyword_list_set in CATEGORY_DICT.items():
        for k_type, keyword_list in keyword_list_set.items():
            if k_type == "restrict":
                for keyword in keyword_list:
                    if any([el == keyword for el in word.lower().split()]):
                        return category
            elif k_type == "lazy":
                for keyword in keyword_list:
                    if word.find(keyword)>-1:
                        return category
    return None

def get_category_list(keyword_list):

        category_set = set()
        category_list = []
        for keyword, compound_noun_list in keyword_list.items():
            for compound_noun in compound_noun_list:
                category = find_category(compound_noun)
                if category:
                    category_set.add(category)
                    break
        if not category_set:
            category_list = ['Miscellaneous']
        else:
            category_list = list(category_set)
        return category_list

def get_category_from_summary(summary):

        category_set = set()
        category_list = []
        for category, keyword_list_set in CATEGORY_DICT.items():
            for k_type, keyword_list in keyword_list_set.items():
                if k_type == "restrict":
                    for keyword in keyword_list:
                        if any([el == keyword for el in summary.lower().split()]):
                            category_set.add(category)
                elif k_type == "lazy":
                    for keyword in keyword_list:
                        if summary.find(keyword)>-1:
                            category_set.add(category)
        if not category_set:
           category_list = ['Miscellaneous']
        else:
           category_list = list(category_set)
        return category_list

def main():
    with open(json_file) as r:           
        data = json.loads(r.read())
        for title, datum in data.items():
            category_list = []
            category_list.extend(get_category_list(datum['keyword_list']))
            category_list.extend(get_category_from_summary(datum['summary']))
            datum['category'] = list(set(category_list))
            if len(datum['category']) > 1 and 'Miscellaneous' in datum['category']:
                datum['category'] = [ 
                        category for category in datum['category'] 
                        if category != 'Miscellaneous'
                    ]
        
        for title, datum in data.items():
            print(f"{title} category is {datum.get('category')}")
    
    with open(json_file, 'w') as w:
        w.write(json.dumps(data))

if __name__ == '__main__':
    main()

                

            

