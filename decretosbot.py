import tweepy, time, sys, json
from decretos import decretos, write_output, get_output
from datetime import date, datetime
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

jsonfile = json.loads(get_output())

for i in jsonfile:
    if len(i['descripcion'])>250:
        try:
            api.update_status("%s %s"%(i['descripcion'][:250], i['link']))
        except tweepy.TweepError as error:
            if error.api_code != 187:
                raise error
    else:
        try:
            api.update_status("%s %s"%(i['descripcion'], i['link']))
        except tweepy.TweepError as error:
            if error.api_code != 187:
                raise error