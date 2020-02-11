import json
import pandas as pd
from TweetModel import Tweet

filename = ('../example_data/twitterq=AnnArbor09-17-2019_0756pm.txt')

with open(filename) as json_file:
    data = json.load(json_file)

for i in data['statuses']:
    newTweet = Tweet(tweetCreator=i['user']['screen_name'],
                     tweetText=i['text'],
                     creatorFollowers=i['user']['followers_count'],
                     mentions=i['entities']['user_mentions'],
                     dateCreated=pd.to_datetime(i['created_at']),
                     tweetID=i['id'],
                     tweetLikes=i['favorite_count'],
                     tweetRe=i['retweet_count']).save()

# Stores screen name into MongoDB
# newTweet = Tweet(tweetCreator=data['statuses'][0]['user']['screen_name']).save()