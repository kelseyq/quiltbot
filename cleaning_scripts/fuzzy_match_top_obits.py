#!/usr/bin/env python

import json
from shutil import copyfile
from os import rename
import datetime
import time
import add_link


def format_for_manual(obit_link, full_name, matches):
    result = (full_name, "./add_link.py " + obit_link + " " + "|".join(matches),
        "../bot/tweet_block.py " + " ".join([match.split(":")[0] for match in matches]))
    return result

with open('../cleaned_quiltdata/items.json', 'r+') as qf:
    with open('../cleaned_quiltdata/top-obit-items.json', 'r+') as of:
        obit_items = json.load(of)
        quilt_items = json.load(qf)
        millis_start = int(round(time.time() * 1000))
        questionable = []

        def check_all_blocks(obit, title_names, full_names):
            matches = []
            q_matches = []
            for item in quilt_items:
                    for block_name in item['names']:
                        quilt_names = set([name for name in block_name['normalized'].split(' ') if len(name) > 2])
                        if len(quilt_names) > 1 and not block_name.get('link') and not obit.get('dupe'):
                            if set(title_names).issubset(quilt_names) or set(full_names).issubset(quilt_names) or \
                                    quilt_names.issubset(full_names):
                                if len(full_names) > 2 and len(block_name['name'].split(' ')) > 2:
                                    q_matches.append(item['block_number'] + ":" + block_name['name'])
                                else:
                                    matches.append(item['block_number'] + ":" + block_name['name'])
            if q_matches:
                questionable.append(format_for_manual(obit['link'], obit['full_name'], q_matches))
            if matches:
                questionable.append(format_for_manual(obit['link'], obit['full_name'], matches))

        for idx, obit in enumerate(obit_items):
            if idx % 100 == 0:
                print("checking obits " + str(idx) + " to " + str(idx + 100))
            obit_title_names = obit['title_name'].split(' ')
            obit_full_names = obit['full_name'].upper().split(' ')
            obit_full_names = [name.replace(".", "").replace("\"", "").replace("'", "") for name in obit_full_names]
            #exclude single names & only initials
            if len(obit_title_names) > 1 and len([name for name in obit_title_names if len(name) > 1]) > 1:
                check_all_blocks(obit, obit_title_names, obit_full_names)

        # copyfile('../cleaned_quiltdata/items.json', '../cleaned_quiltdata/older_data/before_fuzzy_match_top_obits' +
        #          str(datetime.datetime.now()).split('.')[0] + ".json")
        # with open('../cleaned_quiltdata/items2.json', 'w') as f2:
        #     json.dump(quilt_items, f2, indent=2, sort_keys=True)
        #     rename('../cleaned_quiltdata/items2.json', '../cleaned_quiltdata/items.json')

print(len(questionable), " blocks possibly linked to obituaries")
print("#####NEED REVIEW#####")
print('\n\n'.join('\n'.join(pair) for pair in questionable))
elapsed = int(round(time.time() * 1000)) - millis_start
print("Time elapsed: " + str(elapsed) + "ms")
