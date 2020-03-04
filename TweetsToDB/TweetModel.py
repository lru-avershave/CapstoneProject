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
    dateCreated = DateTimeField()

    def json(self):
        tweet_dict = {
            "tweetID": self.tweetID,
            "tweetCreator": self.tweetCreator,
            "tweetText": len(self.tweetText),
            "tweetLikes": self.tweetLikes,
            "tweetRe": self.tweetRe,
            "creatorFollowers": self.creatorFollowers,
            "location": self.location,
            "dateCreated": self.dateCreated
        }
        return json.dumps(tweet_dict)

    meta = {'indexes': [
        {'fields': ['$tweetText'],
            'default_language': 'english',
            'weights': {'tweetText': 10}
        }
    ]}
