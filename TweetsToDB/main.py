import mongodb_setup as dbConnection
import TweetModel as TweetModel
import ImportText as it

class main():

    try:
        dbConnection
        it
    except KeyboardInterrupt:
        print("Interrupted Main")
        exit(0)