import json
from shutil import copyfile
from os import rename
import datetime

#near matches in TOP obits
with open('../cleaned_quiltdata/top-obit-items.json', 'r') as new:
    with open('../cleaned_quiltdata/top-obit-items-no-full-names.json', 'r') as old:
        old_obits = json.load(old)
        new_obits = json.load(new)

        for old_obit in old_obits:
            link = old_obit['link']
            match = next((new_obit for new_obit in new_obits if new_obit['link'] == link), None)
            if not match:
                print("adding", old_obit['full_name_raw'])
                old_obit['full_name'] = ""
                old_obit['title_name'] = old_obit.pop('full_name_raw')
                new_obits.append(old_obit)

        copyfile('../cleaned_quiltdata/top-obit-items.json', '../cleaned_quiltdata/older_data/before_merge_top_obits' +
             str(datetime.datetime.now()).split('.')[0] + ".json")
        with open('../cleaned_quiltdata/top-obit-items2.json', 'w') as f2:
            json.dump(new_obits, f2, indent=2, sort_keys=True)
            rename('../cleaned_quiltdata/top-obit-items2.json', '../cleaned_quiltdata/top-obit-items.json')