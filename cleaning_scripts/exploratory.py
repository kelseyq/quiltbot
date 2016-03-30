import json
import re
from shutil import copyfile
from os import rename
import datetime

#longer than 140 chars
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    for item in items:
        if next((name for name in item['names'] if len(name) > 140), None):
            print(item)

#incorrectly stripped quote
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    i = 0
    for item in items:
        if next((name for name in item['names'] if name.count("\"") % 2 == 1), None):
            print(item)
            i = i + 1
    print(i)

#special characters
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    for item in items:
        for name in item['names']:
            if re.search(r'[\x80-\xFF]', name):
                print(item['block_number'] + ": " + name)

#duplicate names
with open('../cleaned_quiltdata/items.json', 'r+') as f:
    copyfile('../cleaned_quiltdata/items.json', '../cleaned_quiltdata/older_data/before_dedupe_' +
             str(datetime.datetime.now()).split('.')[0] + ".json")
    items = json.load(f)
    i = 0
    for item in items:
        names = item['names']
        if len(names) != len(set(names)):
            dupes = set([name for name in names if len(name.split(" ")) > 1 and names.count(name) > 1])
            if len(dupes) > 0:
                seen = set()
                deduped = [x for x in names if not (x in seen or seen.add(x))]
                item['names'] = deduped
                print("deduped: " + item['block_number'])
                i = i + 1
    print(str(i) + " items deduped")
    with open('../cleaned_quiltdata/items2.json', 'w') as f2:
        json.dump(items, f2, indent=2, sort_keys=True)
        rename('../cleaned_quiltdata/items2.json', '../cleaned_quiltdata/items.json')