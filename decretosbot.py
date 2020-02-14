import tweepy, time, sys, json
from decretos import connection, write_output
from datetime import date, datetime
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

write_output()

def maketweet():
    db=connection()
    tweet=db.decretos.find({"tweet":False})
    if tweet.count()!=0:
        for i in tweet:
            try:
                api.update_status("%s %s"%(i['descripcion'][:250], i['link']))
                db.decretos.update_one(i, {"$set": { "tweet": True}})
            except tweepy.TweepError as error:
                if error.api_code != 187:
                    raise error
    else:
        tweet=db.decretos.find().sort("decreeId",-1).limit(5)
        for i in tweet:
            try:
                api.update_status("%s %s"%(i['descripcion'][:250], i['link']))
            except tweepy.TweepError as error:
                if error.api_code != 187:
                    raise error

maketweet()