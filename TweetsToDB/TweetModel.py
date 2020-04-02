from mongoengine import *
import json

class Tweet(Document):
    tweetID = IntField()
    tweetCreator = StringField()
    tweetText = StringField()
    tweetTextCount = IntField()
    tweetLikes = IntField()
    tweetRe = IntField()
    creatorFollowers = IntField()
    mentions = ListField()
    location = StringField()
    dateCreated = StringField()

    meta = {'indexes': [
        {'fields': ['$tweetText'],
            'default_language': 'english',
            'weights': {'tweetText': 10}
        }
    ]}
