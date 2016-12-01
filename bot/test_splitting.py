import json
import sys
import tweet_block
import time


with open('../cleaned_quiltdata/items.json', 'r') as f:
    items = json.load(f)
    names_total = 0
    names_with_links = 0
    blocks_with_links = 0
    unique_links = set()
    unique_names = set()
    millis_start = int(round(time.time() * 1000))
    for block_number in range(1, len(items)):
        try:
            block_data = next((item for item in items if item['block_number'] == ('%05d' % block_number)))
            names = block_data['names']
            names_total = names_total + len(names)
            block_has_link = False
            for name in names:
                unique_names.add(name.get('normalized'))
                if name.get('link'):
                    block_has_link = True
                    unique_links.add(name.get('link'))
                    names_with_links += 1
            tweet_block.split_names(names)
            if block_has_link:
                blocks_with_links += 1
            if block_number % 100 == 0:
                print("testing blocks " + str(block_number) + " to " + str(block_number + 100))
        except:
            e = sys.exc_info()[0]
            print(e)
            print(block_number)
    elapsed = int(round(time.time() * 1000)) - millis_start
    print("Time elapsed: " + str(elapsed) + "ms")
    print("Names: " + str(names_total))
    print("Links: " + str(names_with_links))
    print("Blocks with links: " + str(names_with_links))
    print("Unique links: " + str(len(unique_links)))
    print("Unique names: " + str(len(unique_names)))
    print("Percent names with links: " + str(names_with_links/names_total * 100) + "%")
    print("Percent blocks with links: " + str(blocks_with_links/len(items) * 100) + "%")