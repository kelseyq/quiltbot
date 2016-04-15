#!/usr/bin/env python

import json
from shutil import copyfile
from os import rename
import datetime
import sys

def add_link_to_blocks(items, link, input):
    blocknames = input.strip().split('|')
    for blockname in blocknames:
        (block_number, target_name) = blockname.split(":",1)
        block_data = next((item for item in items if item['block_number'] == block_number.zfill(5)))
        name = next((name for name in block_data['names'] if name['name'] == target_name))
        if not name.get('link'):
            print("adding link to block", block_number)
            name['link'] = link

#first arg: link
#rest of args: "block:name" separated with |
def main():
    link = ""
    input = ""

    if len(sys.argv) > 1:
        link = sys.argv[1]
        if len(sys.argv) > 2:
            input = sys.argv[2]

    if len(link) == 0:
        std_in = sys.stdin.readline().split(' ', 1)
        link = std_in[0]
        input = std_in[1]
    elif len(input) == 0:
        input = sys.stdin.readline()

    with open('../cleaned_quiltdata/items.json', 'r+') as f:
        items = json.load(f)
        add_link_to_blocks(items, link, input)

        copyfile('../cleaned_quiltdata/items.json', '../cleaned_quiltdata/older_data/before_add_link' +
                 str(datetime.datetime.now()).split('.')[0] + ".json")
        with open('../cleaned_quiltdata/items2.json', 'w') as f2:
            json.dump(items, f2, indent=2, sort_keys=True)
            rename('../cleaned_quiltdata/items2.json', '../cleaned_quiltdata/items.json')

if __name__ == "__main__":
    main()