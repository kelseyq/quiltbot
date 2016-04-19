import json
from shutil import copyfile
from os import rename
import datetime

#near matches in BAR obits
with open('../cleaned_quiltdata/bar-obit-items.json', 'r') as f:
    obits = json.load(f)
    dupes = 0
    for idx, obit in enumerate(obits):
        name = obit['full_name'].split(" ")[:2]
        for i in range(idx + 1, len(obits)):
            if obits[i]['full_name'].split(" ")[:2] == name:
                print(obit['full_name'], "&", obits[i]['full_name'])
                obits[idx]['dupe'] = True
                obits[i]['dupe'] = True
                dupes = dupes + 1
    print(str(dupes), "near duplicate obit names")

    copyfile('../cleaned_quiltdata/bar-obit-items.json', '../cleaned_quiltdata/older_data/before_fuzzy_match_obits' +
         str(datetime.datetime.now()).split('.')[0] + ".json")
    with open('../cleaned_quiltdata/bar-obit-items.json', 'w') as f2:
        json.dump(obits, f2, indent=2, sort_keys=True)
        rename('../cleaned_quiltdata/bar-obit-items.json', '../cleaned_quiltdata/bar-obit-items.json')