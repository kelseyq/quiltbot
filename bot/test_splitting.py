import json
import sys
import tweet_block

with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    for block_number in range(1, 5930):
        try:
            block_data = next((item for item in items if item['block_number'] == ('%05d' % block_number)))
            names = block_data['names']
            tweet_block.split_names(names)
            if block_number % 100 == 0:
                print("testing blocks " + str(block_number) + " to " + str(block_number + 100))
        except:
            e = sys.exc_info()[0]
            print(e)
            print(block_number)