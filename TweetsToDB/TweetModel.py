from mongoengine import *

class Tweet(Document):
    tweetCreator = StringField()
    tweetText = StringField()
    creatorFollowers = IntField()
    mentions = ListField()
    createLocation = StringField()
    dateCreated = DateTimeField()