import pandas as pd
from pandas.io.json import json_normalize
from mongoengine import *
from TweetModel import Tweet
import json

#Need to create a dataframe in order to compute stats

class Stats:
    def __init__(self):
        reqTweet = Tweet.objects().to_json()
        test = json.loads(reqTweet)
        normalTest = json_normalize(test)
        self.df = pd.DataFrame(normalTest)

    def meanRetweets(self):
        print(self.df['tweetRe'].mean())

    def medianRetweets(self):
        print(self.df['tweetRe'].median())

    def modeRetweets(self):
        print(self.df['tweetRe'].mode())


# def statsByCity(term, other filters): 
#     TweetsByTerm+Filters+Sort
#     Total --> Save As Row (Number of tweets, Mean, Median, Mode, blahblahlbah)
#     LenList
#     Loop Total for City --> Append data for specific city to a list --> Save As Row
#     Sort Profile
#     Loop Total for Profiles --> Use the same logic for city

