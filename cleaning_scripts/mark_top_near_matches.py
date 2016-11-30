import json
from shutil import copyfile
from os import rename
import datetime

#near matches in TOP obits
with open('../cleaned_quiltdata/top-obit-items.json', 'r') as f:
    obits = json.load(f)
    dupes = 0
    for idx, obit in enumerate(obits):
        name = obit['title_name']
        for i in range(idx + 1, len(obits)):
            if obits[i]['title_name'] == name:
                obits[idx]['dupe'] = True
                obits[i]['dupe'] = True
                dupes = dupes + 1
    print(str(dupes), "duplicate obit names")

    copyfile('../cleaned_quiltdata/top-obit-items.json', '../cleaned_quiltdata/older_data/before_top_mark_dupes' +
         str(datetime.datetime.now()).split('.')[0] + ".json")
    with open('../cleaned_quiltdata/top-obit-items2.json', 'w') as f2:
        json.dump(obits, f2, indent=2, sort_keys=True)
        rename('../cleaned_quiltdata/top-obit-items2.json', '../cleaned_quiltdata/top-obit-items.json')