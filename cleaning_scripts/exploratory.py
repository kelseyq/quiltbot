import json

#longer than 140 chars
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    for item in items:
        if next((name for name in item['names'] if len(name) > 140), None):
            print(item)

# #contains comma
# with open('../cleaned_quiltdata/items.json', 'r') as f:
#     items = json.load(f)
#     for item in items:
#         name = next((name for name in item['names'] if "," in name), None)
#         if name:
#             print(name)

#incorrectly stripped quote
with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    i = 0
    for item in items:
        if next((name for name in item['names'] if name.count("\"") % 2 == 1), None):
            print(item)
            i = i + 1
    print(i)