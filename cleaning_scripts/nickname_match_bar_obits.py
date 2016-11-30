#!/usr/bin/env python

import json
from shutil import copyfile
from os import rename
import datetime
import time
import add_link

def format_for_manual(obit_link, matches):
   return ("./add_link.py " + obit_link + " '" + "|".join(matches) + "'",
    "../bot/tweet_block.py " + " ".join([match.split(":")[0] for match in matches]))

with open('../cleaned_quiltdata/items.json', 'r+') as qf:
    with open('../cleaned_quiltdata/bar-obit-items.json', 'r+') as of:
        obit_items = json.load(of)
        quilt_items = json.load(qf)
        millis_start = int(round(time.time() * 1000))
        questionable = []

        def check_all_blocks(obit):
            matches = []
            for item in quilt_items:
                    for block_name in item['names']:
                        names_on_block = [name for name in block_name['normalized'].split(' ') if len(name) > 2]
                        if len(set(names_on_block)) > 1:
                            if (len(obit_names) > 2 and [obit_names[-1], obit_names[0]] == names_on_block) or \
                                    (len(obit_names) > 3 and [obit_names[-2], obit_names[-1], obit_names[0]] == names_on_block) or \
                                    (len(obit_names) > 3 and [obit_names[-2], obit_names[0]] == names_on_block):
                                if not block_name.get('link'):
                                    matches.append(item['block_number'] + ":" + block_name['name'])

            if matches:
                questionable.append(format_for_manual(obit['link'], matches))

        for idx, obit in enumerate(obit_items):
            if idx % 100 == 0:
                print("checking obits " + str(idx) + " to " + str(idx + 100))
            obit_names = obit['full_name'].split(' ')
            #exclude single names & only initials
            if len(obit_names) > 1 and len([name for name in obit_names if len(name) > 1]) > 0:
                check_all_blocks(obit)

print("#####NEED REVIEW#####")
print('\n\n'.join('\n'.join(pair) for pair in questionable))
elapsed = int(round(time.time() * 1000)) - millis_start
print("Time elapsed: " + str(elapsed) + "ms")
