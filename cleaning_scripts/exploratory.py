import json
import re

#longer than 140 chars
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    for item in items:
        if next((name for name in item['names'] if len(name['name']) > 140), None):
            print(item)

#incorrectly stripped quote
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    i = 0
    for item in items:
        if next((name for name in item['names'] if name['name'].count("\"") % 2 == 1), None):
            print(item)
            i = i + 1
    print(i, "items with incorrectly stripped quotes")

#more than one comma
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    i = 0
    for item in items:
        for name in item['names']:
            if name['name'].count(',') > 1:
                #print(name['name'])
                i = i + 1
    print(str(i), "names with more than one comma")

#special characters
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    i = 0
    for item in items:
        for name in item['names']:
            if re.search(r'[\x80-\xFF]', name['name']):
                #print(item['block_number'] + ": " + name)
                i = i + 1
    print(str(i) + (" names with special characters"))

#has "and"
#run with 'and' and '&'
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    i = 0
    for item in items:
        for name in item['names']:
            pair = re.search(r'(.+) & (.+)', name['name'])
            if pair:
                i = i + 1
                #print(item['block_number'] + ": " + name['name'])
    print(str(i) + " names with 'and'")

#duplicate names in BAR obits
with open('../cleaned_quiltdata/bar-obit-items.json', 'r') as f:
    obits = json.load(f)
    dupes = 0
    for idx, obit in enumerate(obits):
        name = sorted(obit['full_name'])
        for i in range(idx + 1, len(obits)):
            if sorted(obits[i]['full_name']) == name:
                print(obit['full_name'])
                dupes = dupes + 1
    print(str(dupes), "duplicate obit names")