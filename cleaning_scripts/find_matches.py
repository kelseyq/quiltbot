import json
import sys
import re

#pipe to tweet_block to check multiple candidate blocks
#output: block_number:name, separated by |
with open('../cleaned_quiltdata/items.json', 'r+') as f:
    pattern_string = " ".join(sys.argv[1:])
    pattern = re.compile(pattern_string, re.IGNORECASE)
    items = json.load(f)
    i = 0
    matches = []
    for item in items:
        for name in item['names']:
            if pattern.search(name['name']):
                matches.append(item['block_number'] + ":" + name['name'])
    if len(matches):
        print("|".join(matches))