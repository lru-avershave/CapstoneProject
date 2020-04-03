from mongoengine import Document, IntField, StringField, ListField
import json

class Tweet(Document):
    tweetID = IntField(unique=True)
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
            'default_language': 'none',
            'weights': {'tweetText': 10}
        }
    ]}
