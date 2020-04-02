import mongodb_setup as dbConnection
import TweetModel as TweetModel
# from watchdir import watch
from ImportText import collectTxt

class main():

    try:
        dbConnection
        collectTxt()
        # watch()
    except KeyboardInterrupt:
        print("Interrupted Main")
        exit(0)