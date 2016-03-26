from twython import Twython
import random
import json
import sys

APP_KEY = ''
APP_SECRET = ''
TOKEN = ""
TOKEN_SECRET = ""
PICTURE_DIR = "../cleaned_quiltdata/quilt_images2/full/"

def split_names(names, last_tweet=None):
    while len(names) > 0:
        next_tweet = ""
        while len(next_tweet) < 140:
            if len(names) == 0 or len(next_tweet) + 2 + len(names[0]) > 140:
                break
            if len(next_tweet) > 0:
                next_tweet = next_tweet + "; "
            next_tweet = next_tweet + names[0]
            names.pop(0)
        if last_tweet is not None:
            last_tweet = twitter.update_status(status=next_tweet,
                                                in_reply_to_status_id=last_tweet['id_str'])

def main():
    with open('../cleaned_quiltdata/items.json', 'r') as f:
        items = json.load(f)
        if len(sys.argv) > 1:
            block_number = sys.argv[1].zfill(5)
        else:
            block_number = '%05d' % random.randint(1, 5929)
        block_data = next((item for item in items if item['block_number'] == block_number))
        block_image = open(PICTURE_DIR + block_number + '.jpg', 'rb')
        names = block_data['names']

        twitter = Twython(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)
        response = twitter.upload_media(media=block_image)
        last_tweet = twitter.update_status(status="", media_ids=[response['media_id']])

        split_names(names, last_tweet)

if __name__ == "__main__":
    main()