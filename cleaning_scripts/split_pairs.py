import json
from shutil import copyfile
from os import rename
import datetime
import re

#split pairs and remove duplicate pairs
#does not preserve links
#run with 'and' and '&'
with open('../cleaned_quiltdata/items.json', 'r+') as f:
    copyfile('../cleaned_quiltdata/items.json', '../cleaned_quiltdata/older_data/before_split_pairs' +
             str(datetime.datetime.now()).split('.')[0] + ".json")
    items = json.load(f)
    i = 0
    for item in items:
        for idx, name in enumerate(item['names']):
            pair = re.search(r'(.+) & (.+)', name['name'])
            if pair:
                name_1 = pair.group(1)
                name_2 = pair.group(2)
                dupe = next((i for (i, name) in enumerate(item['names'][idx:]) if name['name'] == name_2 + ' & ' + name_1), None)
                if dupe:
                    i = i + 1
                    item['names'][idx]['name'] = name_1
                    item['names'][dupe+idx]['name'] = name_2
    print("split " + str(i) + " pairs")
    with open('../cleaned_quiltdata/items2.json', 'w') as f2:
        json.dump(items, f2, indent=2, sort_keys=True)
        rename('../cleaned_quiltdata/items2.json', '../cleaned_quiltdata/items.json')