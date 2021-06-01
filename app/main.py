from typing import Optional

from fastapi import FastAPI

import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

import tweepy

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
format = "%a %b %d %H:%M:%S +0000 %Y"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


app = FastAPI()


def twtime(tweet):
    return str(datetime.strptime(tweet['created_at'], format))


def fetchtweets(user_id, count):
    public_tweets = api.user_timeline(user_id=user_id, count=count, tweet_mode="extended")
    tweets = []
    for i in range(len(public_tweets)):
        tweet = public_tweets[i]._json
        tweet["time"] = twtime(tweet)
        tweets.append(tweet)
    return tweets


def fetchfriends(user):
    friends = user.friends()
    friendlist = []
    for i in range(len(friends)):
        friendlist.append(friends[i]._json)
    return friendlist


@app.get("/api/v1/user/{user_name}/friends")
def get_friends(user_name: str):
    try:
        user = api.get_user(user_name)
        return fetchfriends(user)
    except tweepy.TweepError:
        return {'code': 50, 'message': 'User not found.'}



@app.get("/api/v1/user/{user_name}")
def get_user(user_name: str):
    try:
        user = api.get_user(user_name)
        return user._json
    except tweepy.TweepError:
        return {'code': 50, 'message': 'User not found.'}



@app.get("/api/v1/tweets/{user_id}")
def get_tweets(user_id: int, count: Optional[int] = 100):
    return fetchtweets(user_id=user_id, count=count)


@app.get("/api/v1/tweets/{user_id}/{count}")
def get_tweets(user_id: int, count: Optional[int] = 100):
    return fetchtweets(user_id=user_id, count=count)


