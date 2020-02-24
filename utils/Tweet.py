from models.SavedPage import SavedPage
from TweetsToDB.TweetModel import Tweet
from mongoengine import *

def GetTweet(_id):
    reqPage = list(SavedPage.objects(id=_id).aggregate([
        {
            "$project": {
            "_id": "$$REMOVE",
            "pageType": "$$REMOVE",
            "filterTerm": {
                "$cond": {
                    "if": { "$eq": [ "", "$filterTerm" ]},
                    "then": "$$REMOVE",
                    "else": "$filterTerm"
                }
            },
            "filterTime": {
                "$cond": {
                    "if": { "$eq": [ "", "$filterTime" ]},
                    "then": "$$REMOVE",
                    "else": "$filterTime"
                }
            },
            "location": {
                "$cond": {
                    "if": { "$eq": [ "", "$location" ]},
                    "then": "$$REMOVE",
                    "else": "$location"
                }
            },
            "tweetCreator": {
                "$cond": {
                    "if": { "$eq": [ "", "$tweetCreator" ]},
                    "then": "$$REMOVE",
                    "else": "$tweetCreator"
                }
            }
            }
        }
    ]))
    searchStrings = reqPage[0].copy()
    if "filterTerm" in searchStrings:
        filterTerm = searchStrings["filterTerm"]
        del searchStrings["filterTerm"]
        reqTweet = Tweet.objects(__raw__ = searchStrings).search_text(filterTerm)
    else:
        reqTweet = Tweet.objects(__raw__ = searchStrings)

    return reqTweet, reqPage