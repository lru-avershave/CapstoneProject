from models.SavedPage import SavedPage
from TweetsToDB.TweetModel import Tweet
from mongoengine import *
import copy
import re
import datetime

def GetTweet(_id):
    '''
    This retreives the Tweets from the database. We use an aggregate function in order to produce a 'clean' search string.
    This returns both the list of Tweets and the filters used to find the Tweet from our database.
    '''
    searchStrings = list(SavedPage.objects(id=_id).aggregate([
        {
            "$project": {
            "_id": "$$REMOVE",
            "pageType": "$$REMOVE",
            "timestamp": "$$REMOVE",
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
            },
            "filterDate": {
                "$cond": {
                    "if": { "$eq": [ "", "$filterDate" ]},
                    "then": "$$REMOVE",
                    "else": "$filterDate"
                }
            }
            }
        }
    ]))
    returnStrings = copy.deepcopy(searchStrings)
    if "filterDate" in searchStrings[0].keys():
        filterDate = datetime.datetime.strptime(searchStrings[0]["filterDate"], "%Y-%m-%d").strftime("%B %A %d %Y")
        dateList = re.sub("[^\w]", " ",  filterDate).split()
    if "filterTerm" in searchStrings[0].keys() and "filterTime" in searchStrings[0].keys() and "filterDate" in searchStrings[0].keys():
        filterTerm = searchStrings[0]["filterTerm"]
        filterTime = searchStrings[0]["filterTime"]
        del searchStrings[0]["filterTerm"]
        del searchStrings[0]["filterTime"]
        del searchStrings[0]["filterDate"]
        reqTweet = Tweet.objects(__raw__ = searchStrings[0]).search_text(filterTerm)
        reqTweet = reqTweet(dateCreated__icontains=filterTime)
        for word in dateList:
            reqTweet = reqTweet(dateCreated__icontains=word)
    elif "filterTerm" in searchStrings[0].keys() and "filterTime" in searchStrings[0].keys():
        filterTerm = searchStrings[0]["filterTerm"]
        filterTime = searchStrings[0]["filterTime"]
        del searchStrings[0]["filterTerm"]
        del searchStrings[0]["filterTime"]
        reqTweet = Tweet.objects(__raw__ = searchStrings[0]).search_text(filterTerm)
        reqTweet = reqTweet(dateCreated__icontains=filterTime)
    elif "filterDate" in searchStrings[0].keys() and "filterTime" in searchStrings[0].keys():
        filterTerm = searchStrings[0]["filterDate"]
        filterTime = searchStrings[0]["filterTime"]
        del searchStrings[0]["filterDate"]
        del searchStrings[0]["filterTime"]
        reqTweet = Tweet.objects(__raw__ = searchStrings[0])
        reqTweet = reqTweet(dateCreated__icontains=filterTime)
        for word in dateList:
            reqTweet = reqTweet(dateCreated__icontains=word)
    elif "filterDate" in searchStrings[0].keys() and "filterTerm" in searchStrings[0].keys():
        filterTerm = searchStrings[0]["filterTerm"]
        del searchStrings[0]["filterTerm"]
        del searchStrings[0]["filterDate"]
        reqTweet = Tweet.objects(__raw__ = searchStrings[0]).search_text(filterTerm)
        for word in dateList:
            reqTweet = reqTweet(dateCreated__icontains=word)
    elif "filterDate" in searchStrings[0].keys():
        del searchStrings[0]["filterDate"]
        reqTweet = Tweet.objects(__raw__ = searchStrings[0])
        for word in dateList:
            reqTweet = reqTweet(dateCreated__icontains=word)
    elif "filterTerm" in searchStrings[0].keys():
        filterTerm = searchStrings[0]["filterTerm"]
        del searchStrings[0]["filterTerm"]
        reqTweet = Tweet.objects(__raw__ = searchStrings[0]).search_text(filterTerm)
    elif "filterTime" in searchStrings[0].keys():
        filterTime = searchStrings[0]["filterTime"]
        del searchStrings[0]["filterTime"]
        reqTweet = Tweet.objects(__raw__ = searchStrings[0])
        reqTweet = reqTweet(dateCreated__contains=filterTime)
    else:
        reqTweet = Tweet.objects(__raw__ = searchStrings[0])
    return reqTweet, returnStrings