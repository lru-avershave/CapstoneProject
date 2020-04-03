from mongoengine import Document, IntField, StringField, ListField
import json

class Tweet(Document):
    '''
    Schema for the Tweet document. Can be expanded in the future if needed.
    '''
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

    '''
    The default_language is set to none because of a known bug of not being able to search for common words.
    '''
    meta = {'indexes': [
        {'fields': ['$tweetText'],
            'default_language': 'none',
            'weights': {'tweetText': 10}
        }
    ]}
