import pandas as pd
from pandas.io.json import json_normalize
from TweetsToDB.TweetModel import Tweet
import json

#Need to create a dataframe in order to compute stats
def statTweets(jsonTweet):
    options = ['tweetLikes', 'tweetRe']
    normalTweet = json_normalize(jsonTweet)
    df = pd.DataFrame(normalTweet)
    stats = []

    for o in options:
        optionStats = []
        optionStats.append(o)
        optionStats.append(df[o].mean())
        optionStats.append(df[o].median())
        optionStats.append(df[o].mode()[0])
        optionStats.append(df[o].mad())
        optionStats.append(df[o].std())

        Q1 = df[o].quantile([0.25][0])
        optionStats.append(Q1)
        Q3 = df[o].quantile([0.75][0])
        optionStats.append(Q3)

        optionStats.append(df[o].max() - df[o].min())
        
        # #Outlier stuff
        iqr = Q3 - Q1 + 5
        lower_bound = Q1 - (1.5 * iqr)
        upper_bound = Q3 + (1.5 * iqr)
        outlierCount = 0
        for value in df[o]:
            if(value < lower_bound) or (value > upper_bound):
                outlierCount += 1
        optionStats.append(outlierCount)
        stats.append(optionStats)

    return stats
