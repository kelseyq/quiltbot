#!/usr/bin/env python

from twython import Twython
import random
import json
import sys
import time
import os

APP_KEY = ''
APP_SECRET = ''
TOKEN = ""
TOKEN_SECRET = ""
PICTURE_DIR = "../cleaned_quiltdata/quilt_images2/full/"


def split_names(names, twitter=None, last_tweet=None):
    while len(names) > 0:
        next_tweet = ""

        #link tweets
        if names[0].get('link'):
            next_name = names.pop(0)
            status = next_name['name'] + "\n" + next_name['link']
            if twitter is not None:
                time.sleep(5)
                twitter.update_status(status=status, in_reply_to_status_id=last_tweet['id_str'])

        while len(next_tweet) < 140:
            if len(names) == 0 \
                    or names[0].get('link') \
                    or len(next_tweet) + 2 + len(names[0]['name']) > 140:
                break
            if len(next_tweet) > 0:
                next_tweet = next_tweet + "; "
            next_tweet = next_tweet + names.pop(0)['name']
        assert len(next_tweet) <= 140

        if twitter is not None and len(next_tweet) > 0:
            time.sleep(5)
            twitter.update_status(status=next_tweet, in_reply_to_status_id=last_tweet['id_str'])

def main():
    with open('../cleaned_quiltdata/items.json', 'r') as f:
        items = json.load(f)
        twitter = Twython(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)

        if len(sys.argv) > 1:
            block_numbers = [number.zfill(5) for number in sys.argv[1:]]
        else:
            blocks_left = len(os.listdir(PICTURE_DIR))
            block_numbers = [os.listdir(PICTURE_DIR)[random.randrange(0, blocks_left)].split('.')[0]]

        for block_number in block_numbers:
            block_data = next((item for item in items if item['block_number'] == block_number))
            block_path = PICTURE_DIR + block_number + '.jpg'
            block_image = open(block_path, 'rb')
            names = block_data['names']

            print("tweeting block", block_number)
            response = twitter.upload_media(media=block_image)
            last_tweet = twitter.update_status(status="", media_ids=[response['media_id']])

            split_names(names, twitter, last_tweet)
            print("deleting block", block_number)
            os.remove(block_path)


if __name__ == "__main__":
    main()