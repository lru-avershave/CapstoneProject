import json
import pandas as pd
import glob
import os
from TweetModel import Tweet
import logging
import pathlib
from mongoengine import NotUniqueError

def TextToTweet(filename):
    '''
    This is what takes the Tweets from the PHP script and puts them into the database using the TweetModel schema.
    It also has some error catching. First, if the data is bad coming from the PHP script, it will not use it. Second, if there's a duplicate Tweet, it will not add it.
    '''
    logging.basicConfig(filename="TextToTweet.log", level=logging.DEBUG, format='%(levelname)s:%(message)s')
    try:
        with open(filename) as json_file:
            data = json.load(json_file)

        query = data['search_metadata']['query']
        if '+' in query:
            query = query.replace('+', ' ')

        for i in data['statuses']:
            try:
                newTweet = Tweet(tweetCreator=i['user']['screen_name'],
                                tweetText=i['text'],
                                creatorFollowers=i['user']['followers_count'],
                                mentions=i['entities']['user_mentions'],
                                dateCreated=i['created_at'],
                                tweetID=i['id'],
                                tweetLikes=i['favorite_count'],
                                tweetRe=i['retweet_count'],
                                tweetTextCount=len(i['text']))
                newTweet.location = query
                newTweet.save()
            except NotUniqueError as e:
                logging.debug('Unique match found: {}'.format(e))
                continue


    except Exception as e:
        logging.debug('Issue with: {}: {}'.format(filename, e))
        pass

def collectTxt():
    '''
    This small function takes the .txt files from whatever dir you change into into Tweet objects into the db.
    This drives this module.
    '''
    os.chdir("C:\\Users\\austi\\OneDrive\\Spring(COVID)\\Text")
    for file in glob.glob('*.txt'):
        TextToTweet(file)