from TweetsToDB.TweetModel import *

def locationCounter(reqTweet):
    locations = reqTweet.distinct("location")
    locationTotals = [] 
    for i in locations:
        locationTotals.append({
                        "location" : i,
                        "count" : reqTweet(location=i).count()
        })
    return locationTotals

