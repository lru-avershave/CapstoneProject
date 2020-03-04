from models.SavedPage import SavedPage
from TweetsToDB.TweetModel import Tweet
from mongoengine import *
import orjson

def GetTweet(_id):
    searchStrings = list(SavedPage.objects(id=_id).aggregate([
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
    if "filterTerm" in searchStrings[0]:
        filterTerm = searchStrings[0]["filterTerm"]
        del searchStrings[0]["filterTerm"]
        reqTweet = Tweet.objects(__raw__ = searchStrings[0]).search_text(filterTerm)
    else:
        reqTweet = Tweet.objects(__raw__ = searchStrings[0])
    return reqTweet, searchStrings