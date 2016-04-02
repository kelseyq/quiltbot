import json
from shutil import copyfile
from os import rename
import datetime
from unidecode import unidecode

with open('../cleaned_quiltdata/items.json', 'r+') as f:
    items = json.load(f)
    for item in items:
        for idx, name in enumerate(item['names']):
            normalized = unidecode(name['name'])
            normalized = normalized.replace(' - ', '-')
            normalized = normalized.upper()
            item['names'][idx]['normalized'] = normalized
    copyfile('../cleaned_quiltdata/items.json', '../cleaned_quiltdata/older_data/before_normalize' +
             str(datetime.datetime.now()).split('.')[0] + ".json")
    with open('../cleaned_quiltdata/items2.json', 'w') as f2:
        json.dump(items, f2, indent=2, sort_keys=True)
        rename('../cleaned_quiltdata/items2.json', '../cleaned_quiltdata/items.json')