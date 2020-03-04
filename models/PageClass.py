import orjson
from app import cache

class Page():
    def __init__(self, reqPage, tweetJson):
        self.reqPage = reqPage
        self.tweetJson = tweetJson

    @cache.cached(timeout=60)
    def getTweet(self):
        return self.tweetJson