from TweetsToDB.TweetModel import *

def dynamicFiltering():
    tempTweet = Tweet.objects()

    dynamicFilters = []
    dynamicFilters.append(locationFiltering(tempTweet))
    dynamicFilters.append(profileFiltering(tempTweet))
    return dynamicFilters

def locationFiltering(tempTweet):
    locationFilters = tempTweet.distinct("location")
    return locationFilters

def profileFiltering(tempTweet):
    profileFilters = tempTweet.distinct("tweetCreator")
    return profileFilters
