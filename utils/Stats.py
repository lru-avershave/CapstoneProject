import pandas as pd
from pandas.io.json import json_normalize
from TweetsToDB.TweetModel import Tweet
import json

#Need to create a dataframe in order to compute stats
def statTweets(jsonTweet):
    options = ['tweetLikes', 'tweetRe']
    normalTweet = json_normalize(jsonTweet)
    df = pd.DataFrame(normalTweet)

    
    mean, median, mode, deviation, variance, quartile1, quartile3, ranges, outliers = [], [], [], [], [], [], [], [], []
    stats = {'mean': None, 'median': None, 'mode': None, 'deviation': None, 'variance': None, 'quartile1': None, 'quartile3': None, "ranges": None,"outliers": None}
    
    for o in options:
        mean.append(df[o].mean())
        median.append(df[o].median())
        mode.append(df[o].mode())
        deviation.append(df[o].mad())
        variance.append(df[o].var)

        Q1 = df[o].quantile([0.25])
        quartile1.append(Q1)
        Q3 = df[o].quantile([0.75])
        quartile3.append(Q3)

        ranges.append(df[o].max() - df[o].min())
        
        #Outlier stuff
        iqr = Q3 - Q1
        lower_bound = Q1 - (1.5 * iqr)
        upper_bound = Q3 + (1.5 * iqr)
        outlierCount = 0
        for value in df[o]:
            if(value < lower_bound) or (value > upper_bound):
                outlierCount += 1
        outliers.append(outlierCount)

    stats['mean'] = dict(zip(options, mean))
    stats['median'] = dict(zip(options, median))
    stats['mode'] = dict(zip(options, mode))
    stats['deviation'] = dict(zip(options, deviation))
    stats['variance'] = dict(zip(options, variance))
    stats['quartile1'] = dict(zip(options, quartile1))
    stats['quartile3'] = dict(zip(options, quartile3))
    stats['ranges'] = dict(zip(options, ranges))
    stats['outliers'] = dict(zip(options, outliers))

    return stats


# def statsByCity(term, other filters): 
#     TweetsByTerm+Filters+Sort
#     Total --> Save As Row (Number of tweets, Mean, Median, Mode, blahblahlbah)
#     LenList
#     Loop Total for City --> Append data for specific city to a list --> Save As Row
