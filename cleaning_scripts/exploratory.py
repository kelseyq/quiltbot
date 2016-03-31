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
    print(i)

#special characters
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    for item in items:
        for name in item['names']:
            if re.search(r'[\x80-\xFF]', name['name']):
                print(item['block_number'] + ": " + name)

