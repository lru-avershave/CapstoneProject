from mongoengine import *

class SavedPage(Document):
    pageType = StringField()
    filterTerm = StringField()
    filterTime = StringField()
    location = StringField()
    tweetCreator = StringField()