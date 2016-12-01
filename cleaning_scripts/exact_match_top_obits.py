#!/usr/bin/env python

import json
from shutil import copyfile
from os import rename
import datetime
import time
import add_link

with open('../cleaned_quiltdata/items.json', 'r+') as qf:
    with open('../intermediate_data/top-obit-items.json', 'r+') as of:
        obit_items = json.load(of)
        quilt_items = json.load(qf)
        millis_start = int(round(time.time() * 1000))
        links = []
        multiples = []
        found = []

        def check_all_blocks(obit, title_names, full_names):
            matches = []
            for item in quilt_items:
                    for block_name in item['names']:
                        quilt_names = [name for name in block_name['normalized'].split(' ') if len(name) > 2]
                        if len(quilt_names) > 1:
                            if (sorted(title_names) == sorted(block_name['normalized'].split(' '))) or \
                                    (len(full_names) > 1 and sorted(full_names) == sorted(block_name['normalized'].split(' '))):
                                if block_name.get('link', None):
                                    links.append((block_name['link'], obit['link']))
                                    return
                                matches.append(item['block_number'] + ":" + block_name['name'])
            if len(matches) > 2:
                multiples.append((obit['link'],
                                  "|".join(matches),
                                  [match.split(":")[0] for match in matches]))
            elif matches:
                for match in matches:
                    found.append(match)
                print("linking", obit['full_name'])
                add_link.add_link_to_blocks(quilt_items, obit['link'], "|".join(matches))

        for idx, obit in enumerate(obit_items):
            if idx % 100 == 0:
                print("checking obits " + str(idx) + " to " + str(idx + 100))
            obit_title_names = obit['title_name'].split(' ')
            obit_full_names = obit['full_name'].upper().split(' ')
            #exclude single names & only initials
            if len(obit_title_names) > 1 and len([name for name in obit_title_names if len(name) > 1]) > 0:
                check_all_blocks(obit, obit_title_names, obit_full_names)

        copyfile('../cleaned_quiltdata/items.json', '../cleaned_quiltdata/older_data/before_match_obits' +
                 str(datetime.datetime.now()).split('.')[0] + ".json")
        with open('../cleaned_quiltdata/items2.json', 'w') as f2:
            json.dump(quilt_items, f2, indent=2, sort_keys=True)
            rename('../cleaned_quiltdata/items2.json', '../cleaned_quiltdata/items.json')

print(len(found), " blocks linked to obituaries")
print("#####ALREADY LINKED#####")
print(links)
print("#####MULTIPLE RESULTS#####")
print(multiples)
elapsed = int(round(time.time() * 1000)) - millis_start
print("Time elapsed: " + str(elapsed) + "ms")
