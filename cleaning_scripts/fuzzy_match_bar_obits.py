#!/usr/bin/env python

import json
from shutil import copyfile
from os import rename
import datetime
import time
import add_link

def format_for_manual(obit_link, matches):
   return ("./add_link.py " + obit_link + " " + "|".join(matches),
    "../bot/tweet_block.py " + " ".join([match.split(":")[0] for match in matches]))

with open('../cleaned_quiltdata/items.json', 'r+') as qf:
    with open('../cleaned_quiltdata/bar-obit-items.json', 'r+') as of:
        obit_items = json.load(of)
        quilt_items = json.load(qf)
        millis_start = int(round(time.time() * 1000))
        links = []
        found = []
        questionable = []

        def check_all_blocks(obit):
            matches = []
            q_matches = []
            for item in quilt_items:
                    for block_name in item['names']:
                        names_on_block = [name for name in block_name['normalized'].split(' ') if len(name) > 2]
                        if len(set(names_on_block)) > 1:
                            #if len(obit_names) > 2 and [obit_names[-1], obit_names[0]] == names_on_block:
                            if list(reversed(obit_names[:2])) == names_on_block:
                                if not block_name.get('link'):
                                    if obit.get('dupe') or len(obit_names) > 2 and len(block_name['name'].split(' ')) > 2:
                                        q_matches.append(item['block_number'] + ":" + block_name['name'])
                                    else:
                                        matches.append(item['block_number'] + ":" + block_name['name'])
                                elif sorted(obit_names) != sorted(block_name['normalized'].split(' ')) and block_name.get('link') != obit['link']:
                                    links.append((obit['full_name'], item['block_number'] + ":" + block_name['name'], (block_name['link'], obit['link'])))

            if q_matches or len(matches) > 1:
                if matches:
                    questionable.append(format_for_manual(obit['link'], matches))
                if q_matches:
                    questionable.append(format_for_manual(obit['link'], q_matches))
            elif matches:
                for match in matches:
                    found.append(match)
                add_link.add_link_to_blocks(quilt_items, obit['link'], "|".join(matches))
                print("linking", obit['full_name'])

        for idx, obit in enumerate(obit_items):
            if idx % 100 == 0:
                print("checking obits " + str(idx) + " to " + str(idx + 100))
            obit_names = obit['full_name'].split(' ')
            #exclude single names & only initials
            if len(obit_names) > 1 and len([name for name in obit_names if len(name) > 1]) > 0:
                check_all_blocks(obit)

        copyfile('../cleaned_quiltdata/items.json', '../cleaned_quiltdata/older_data/before_fuzzy_match_obits' +
                 str(datetime.datetime.now()).split('.')[0] + ".json")
        with open('../cleaned_quiltdata/items2.json', 'w') as f2:
            json.dump(quilt_items, f2, indent=2, sort_keys=True)
            rename('../cleaned_quiltdata/items2.json', '../cleaned_quiltdata/items.json')

print(len(found), " blocks linked to obituaries")
print("#####ALREADY LINKED#####")
print(links)
print("#####NEED REVIEW#####")
print('\n\n'.join('\n'.join(pair) for pair in questionable))
elapsed = int(round(time.time() * 1000)) - millis_start
print("Time elapsed: " + str(elapsed) + "ms")
