from TweetsToDB.TweetModel import *

# Counts the number of tweets per location in the user's query
# Takes in the current query of tweets as a parameter
# Return an array of dictionaries with the location name and the total
def locationCounter(reqTweet):
    locations = reqTweet.distinct("location")
    locationTotals = []

    for i in locations:
        locationTotals.append({
                        "location" : i,
                        "count" : reqTweet(location=i).count()
        })
        
    return locationTotals

