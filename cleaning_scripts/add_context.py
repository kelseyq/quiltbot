import json
from shutil import copyfile
from os import rename
import datetime

#duplicate names
with open('../cleaned_quiltdata/items.json', 'r+') as f:
    copyfile('../cleaned_quiltdata/items.json', '../cleaned_quiltdata/older_data/before_add_context' +
             str(datetime.datetime.now()).split('.')[0] + ".json")
    items = json.load(f)
    i = 0
    for item in items:
        names = item['names']
        name_dict_list = [{'name': name} for name in names]
        item['names'] = name_dict_list
    with open('../cleaned_quiltdata/items2.json', 'w') as f2:
        json.dump(items, f2, indent=2, sort_keys=True)
        rename('../cleaned_quiltdata/items2.json', '../cleaned_quiltdata/items.json')