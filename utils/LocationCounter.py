from TweetsToDB.TweetModel import *

def locationCounter(reqTweet):
       locations = reqTweet.distinct("location") 
       for i in locations:
           locationTotals = {
                            "location" : i
                            "count" : Tweet.objects("location"=i).count()
            }