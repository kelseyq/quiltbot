import json
from shutil import copyfile
from os import rename
import datetime

#duplicate names -- run before supplementary was added
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