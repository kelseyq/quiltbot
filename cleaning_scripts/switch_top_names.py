import json
from shutil import copyfile
from os import rename
import datetime

#switch names in TOP obits
with open('../cleaned_quiltdata/top-obit-items.json', 'r') as f:
    obits = json.load(f)
    new_obits = []
    dupes = 0
    for obit in obits:
        if "&" in obit['title_name'] or (" AND " in obit['title_name']) or (" and " in obit['title_name']):
            pass
        else:
            names = obit['title_name'].split()
            if len(names) == 2:
                pass
                # names.reverse()
                # obit['title_name'] = " ".join(names)
            else:
                names = obit['title_name'].split()
                names.append(names.pop(0))
                obit['title_name'] = " ".join(names)
        new_obits.append(obit)

    copyfile('../cleaned_quiltdata/top-obit-items.json', '../cleaned_quiltdata/older_data/before_top_switch' +
         str(datetime.datetime.now()).split('.')[0] + ".json")
    with open('../cleaned_quiltdata/top-obit-items2.json', 'w') as f2:
        json.dump(obits, f2, indent=2, sort_keys=True)
        rename('../cleaned_quiltdata/top-obit-items2.json', '../cleaned_quiltdata/top-obit-items.json')