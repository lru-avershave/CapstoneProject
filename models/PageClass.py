import orjson

class Page():
    def __init__(self, reqPage, tweetJson):
        self.reqPage = reqPage
        self.tweetJson = tweetJson
    
    def getTweet(self):
        return self.tweetJson