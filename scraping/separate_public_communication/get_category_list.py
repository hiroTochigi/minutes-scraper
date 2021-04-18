import json
import re

CATEGORY_LIST = {
    'Housing': {
        'lazy': ["housing", "tenant", "affordable", "zoning", "eviction", "propert"],
        'restrict': ["aho"]
        },
    'Local Economy': {
        "lazy": ["restaurant", "business"],
        "restrict": []
        },
    'Art': {
        "lazy":["artistic"],
        "restrict": ["art", "arts"]
        },
    'School': {
        "lazy": ["school"],
        "restrict": ["crls"]
        },
    'Bike': {
        "lazy": ["cycling"],
        "restrict": ["bike", "bikes"]
        },
    "Transportation": {
        "lazy": ["parking", "traffic", "pedestrian"],
        "restrict": []
        },
    "Public Transportation": {
        "lazy": [],
        "restrict": ["bus", "buses"]
        },
    "Covid-19": {
        "lazy": ["covid", "mask", "transmission", "ventilation", 'social distance'],
        "restrict": []},
    "Environment": {
        "lazy": ["natural gas", "environment", "vegetation", "animal harm", "climate"],
        "restrict": ["tree", "trees"]
        },
    "Police": {
        "lazy": ["police", "tear gas"],
        "restrict": []
        },
    "Cannabis": {
        "lazy": ["cannabis"],
        "restrict": []
        },
    "Municipal Broadband": {
        "lazy": ["municipal broadband"],
        "restrict": []
        },
    "City Manager": {
        "lazy": ["city manager's contract", "city manager&s contract"],
        "restrict": []
        },
    "Campaign Finance Reform": {
        "lazy": ["campaign finance reform"],
        "restrict": []
        },
    "Racism": {
        "lazy": ["racism"],
        "restrict": []
        },
}

def find_category(word):

    for category, keyword_list_set in CATEGORY_LIST.items():
        for k_type, keyword_list in keyword_list_set.items():
            if k_type == "restrict":
                for keyword in keyword_list:
                    if any([el == keyword for el in word.lower().split()]):
                        return category
            else:
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
        for category, keyword_list_set in CATEGORY_LIST.items():
            for k_type, keyword_list in keyword_list_set.items():
                if k_type == "restrict":
                    for keyword in keyword_list:
                        if any([el == keyword for el in summary.lower().split()]):
                            category_set.add(category)
                else:
                    for keyword in keyword_list:
                        if summary.find(keyword)>-1:
                            category_set.add(category)
        if not category_set:
           category_list = ['Miscellaneous']
        else:
           category_list = list(category_set)
        return category_list

def main():
    with open('all_comment_metadata.json') as r:
        data = json.loads(r.read())
        for title, datum in data.items():
            category_list = []
            category_list.extend(get_category_list(datum['keyword_list']))
            category_list.extend(get_category_from_summary(datum['summary']))
            datum['category'] = list(set(category_list))
            if len(datum['category']) > 1 and 'Miscellaneous' in datum['category']:
                datum['category'] = [ category for category in datum['category'] if category != 'Miscellaneous']
        
        for title, datum in data.items():
            print(f"{title} category is {datum.get('category')}")
    
    with open('all_comment_metadata.json', 'w') as w:
        w.write(json.dumps(data))

if __name__ == '__main__':
    main()

                

            

