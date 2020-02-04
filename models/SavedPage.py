from mongoengine import *

class SavedPage(Document):
    pageType = StringField()
    filterTerm = StringField()
    filterTime = StringField()
    filterLocation = StringField()
    filterProfile = StringField()