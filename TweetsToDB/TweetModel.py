from mongoengine import *

class Tweet(Document):
    tweetID = IntField()
    tweetCreator = StringField()
    tweetText = StringField()
    tweetLikes = IntField()
    tweetRe = IntField()
    creatorFollowers = IntField()
    mentions = ListField()
    location = StringField()
    dateCreated = DateTimeField()

    meta = {'indexes': [
        {'fields': ['$tweetText']},
        'default_language': 'english',
        'weights': {'tweetText': 10}
        }
    ]}
