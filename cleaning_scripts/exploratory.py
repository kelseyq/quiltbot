import json
import re
import os

#longer than 140 chars
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    for item in items:
        if next((name for name in item['names'] if len(name['name']) > 140), None):
            print(item)

#incorrectly stripped quote
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    i = 0
    for item in items:
        if next((name for name in item['names'] if name['name'].count("\"") % 2 == 1), None):
            print(item)
            i = i + 1
    print(i, "items with incorrectly stripped quotes")

#more than one comma
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    i = 0
    for item in items:
        for name in item['names']:
            if name['name'].count(',') > 1:
                # print(name['name'])
                i = i + 1
    print(str(i), "names with more than one comma")

#special characters
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    i = 0
    for item in items:
        for name in item['names']:
            if re.search(r'[\x80-\xFF]', name['name']):
                print(item['block_number'] + " " + name['name'])
                i = i + 1
    print(str(i) + (" names with special characters"))

#has "and"
#run with 'and' and '&'
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    i = 0
    for item in items:
        for name in item['names']:
            pair = re.search(r'(.+) and (.+)', name['name'])
            if pair:
                i = i + 1
               # print(item['block_number'] + ": " + name['name'])
    print(str(i) + " names with 'and'")

# #duplicate names in BAR obits
# with open('../intermediate_data/bar-obit-items.json', 'r') as f:
#     obits = json.load(f)
#     dupes = 0
#     for idx, obit in enumerate(obits):
#         name = sorted(obit['full_name'])
#         for i in range(idx + 1, len(obits)):
#             if sorted(obits[i]['full_name']) == name:
#                 print(obit['full_name'])
#                 dupes = dupes + 1
#     print(str(dupes), "duplicate obit names")

# #duplicate names in TOP obits
# with open('../intermediate_data/top-obit-items.json', 'r') as f:
#     obits = json.load(f)
#     dupes = 0
#     for idx, obit in enumerate(obits):
#         name = obit['title_name']
#         for i in range(idx + 1, len(obits)):
#             if (obits[i]['title_name']) == name:
#                 print(obit['title_name'])
#                 dupes = dupes + 1
#     print(str(dupes), "duplicate obit names")

# names with more than 3 components in TOP obits
with open('../intermediate_data/top-obit-items.json', 'r') as f:
    obits = json.load(f)
    longnames = 0
    for idx, obit in enumerate(obits):
        if "&" in obit['title_name'] or (" AND " in obit['title_name']) or (" and " in obit['title_name']):
            pass
        else:
            names = obit['title_name'].split()
            if len(names) > 2:
                # print(obit['title_name'])
                longnames = longnames + 1
    print(str(longnames), "long names")

#composite obits
with open('../intermediate_data/top-obit-items.json', 'r') as f:
    obits = json.load(f)
    andnames = 0
    for idx, obit in enumerate(obits):
        if "&" in obit['title_name'] or (" AND " in obit['title_name']) or (" and " in obit['title_name']):
            #print(obit['title_name'], obit['link'])
            andnames = andnames + 1
    print(str(andnames), "composite names")

#list missing quilt block images
with open('../cleaned_quiltdata/items.json', 'r') as f:
    obits_string = f.read()
    obits = json.loads(obits_string)
    filenames = os.listdir('../cleaned_quiltdata/quilt_images2/full/')
    missing_images = [obit['block_number'] for obit in obits if obit['block_number'] + ".jpg" not in filenames]
    print(missing_images)
    print("Number of missing images: " + str(len(missing_images)))
    missing_blocks = [filename.split('.')[0] for filename in filenames if filename.split('.')[0] not in obits_string]
    print(missing_blocks)
    print("Number of missing blocks: " + str(len(missing_blocks)))
