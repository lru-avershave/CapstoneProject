import json
import pandas as pd
import glob
import os
from TweetModel import Tweet
import logging
import pathlib

def TextToTweet(filename):
    logging.basicConfig(filename="TextToTweet.log", level=logging.DEBUG, format='%(levelname)s:%(message)s')
    try:
        with open(filename) as json_file:
            data = json.load(json_file)

        query = data['search_metadata']['query']
        if '+' in query:
            query = query.replace('+', ' ')

        for i in data['statuses']:
            newTweet = Tweet(tweetCreator=i['user']['screen_name'],
                            tweetText=i['text'],
                            creatorFollowers=i['user']['followers_count'],
                            mentions=i['entities']['user_mentions'],
                            dateCreated=pd.to_datetime(i['created_at']),
                            tweetID=i['id'],
                            tweetLikes=i['favorite_count'],
                            tweetRe=i['retweet_count'],
                            tweetTextCount=len(i['text']))
            newTweet.location = query
            newTweet.save()

        newTweet.save()
    except Exception as e:
        logging.debug('Issue with: {}'.format(filename))
        pass

def collectTxt():
    os.chdir('C:\\Users\\austi\\Desktop\\Text\\')
    for file in glob.glob('*.txt'):
        TextToTweet(file)