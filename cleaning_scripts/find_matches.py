#!/usr/bin/env python

import json
import sys
import re
import getopt

#pipe to tweet_block or add_link to check multiple candidate blocks
#output: block_number:name, separated by |
with open('../cleaned_quiltdata/items.json', 'r+') as f:
    optlist, args = getopt.getopt(sys.argv[1:], 'p')
    pipe = len(optlist) > 0
    pattern_string = " ".join(args)
    pattern = re.compile(pattern_string, re.IGNORECASE)
    items = json.load(f)
    i = 0
    matches = []
    for item in items:
        for name in item['names']:
            if pattern.search(name['name']):
                if pipe:
                    matches.append(item['block_number'])
                else:
                    matches.append(item['block_number'] + ":" + name['name'])
    if len(matches):
        if pipe:
            print(" ".join(matches))
        else:
            print("|".join(matches))