import requests
import json
import tweepy
import time

print('starting up')
f = open('config.json')
config = json.load(f)

webhook_url = config['webhook_url']

consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']
access_token = config['access_token']
access_secret = config['access_secret']

past_fashion_report_ids = config['past_fashion_report_ids']

f.close()
print('config initialized')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

while True:
    print('grabbing past 50 tweets from kaiyoko')
    cursor = tweepy.Cursor(api.user_timeline, id='KaiyokoStar', tweet_mode='extended').items(30)

    for i in cursor:
        if ('RT'.encode('UTF-8') not in i.full_text.encode('UTF-8')) and 'Full Details'.encode('UTF-8') in i.full_text.encode('UTF-8') and i.id not in past_fashion_report_ids:
            print('sending fashion report to #announcements')
            data = { "content":"<@&878507983116599317>\nhttps://twitter.com/KaiyokoStar/status/"+str(i.id) }
            r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            past_fashion_report_ids.append(i.id)
            config['past_fashion_report_ids'] = past_fashion_report_ids
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
    print('nap time....')
    time.sleep(3600)

    