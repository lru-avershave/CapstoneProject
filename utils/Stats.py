import pandas as pd
from pandas.io.json import json_normalize
from mongoengine import *
from TweetsToDB.TweetModel import Tweet
import json

#Need to create a dataframe in order to compute stats
def statTweets(reqTweet):
    options = ['tweetLikes', 'tweetRe']
    Tweets = reqTweet.to_json()
    jsonTweet = json.loads(Tweets)
    normalTweet = json_normalize(jsonTweet)
    df = pd.DataFrame(normalTweet)
    mean, median, mode = [], [], []
    stats = {'mean': None, 'median': None, 'mode': None}
    for o in options:
        mean.append(df[o].mean())
        median.append(df[o].median())
        mode.append(df[o].mode())
    stats['mean'] = dict(zip(options, mean))
    stats['median'] = dict(zip(options, median))
    stats['mode'] = dict(zip(options, mode))
    return stats


# def statsByCity(term, other filters): 
#     TweetsByTerm+Filters+Sort
#     Total --> Save As Row (Number of tweets, Mean, Median, Mode, blahblahlbah)
#     LenList
#     Loop Total for City --> Append data for specific city to a list --> Save As Row
#     Sort Profile
#     Loop Total for Profiles --> Use the same logic for city

