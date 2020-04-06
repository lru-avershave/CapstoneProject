from mongoengine import StringField, Document

class SavedPage(Document):
    '''
    This is a schema for a page. We're using this as a session for the user. The user can return to this session with a generated ID.
    '''
    pageType = StringField()
    filterTerm = StringField()
    dateCreated = StringField()
    location = StringField()
    tweetCreator = StringField()