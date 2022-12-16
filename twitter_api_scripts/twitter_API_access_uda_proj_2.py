# Before running this script install tweepy 
# put hashtag or search keyword in line 52. Don't use #. If using more than one search word like Biden and Ukraine, use "Biden + Ukraine"
# Two output files are created (lines 48 and 53). tweets.csv  will contain tweets and other information such as location; tweet_network.csv (line 72) has the 3-column file from which a network can be created
# put the number of tweets to fetch in line 23. Change items(500) to the number you want, but I recommend limiting it to 3000 in one search. After a few hours search again.
import tweepy
import pandas as pd
import datetime
import time
import re

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
BEARER_TOKEN = ''



def auth(queryTxt):
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        #api = tweepy.API(auth,wait_on_rate_limit = True)
        #api.update_status("Hello Tweepy")
        clientAPI = tweepy.Client(BEARER_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    except:
        print("An error occurred during the authentication")

    #tweets = tweepy.Cursor(api.search_tweets , q="#" + query, rpp=100).items(500)
    #tweets = tweepy.Cursor(clientAPI.search_recent_tweets, q="#" + query, rpp=100).items(500)
    tweets = clientAPI.search_recent_tweets(queryTxt, tweet_fields=['context_annotations', 'created_at', 'author_id'], expansions='referenced_tweets.id',
        place_fields=['place_type', 'geo'], user_fields=['location'], max_results=100, )
    count = 0
    df = pd.DataFrame(columns=['tweetID', 'created_at', 'location', 'username', 'fixedText'])


    for tweet in tweets.data:
        tweet_id = tweet.id
        created_at = tweet.created_at
        author = tweet.author_id
        user = clientAPI.get_user(id=author, user_fields='location')
        text = tweet.text
        fixed_text = tweet.text

        # whenever a tweet is retweeted, twitter automatically truncates the tweet's text which we don't really want
        # the following code finds the original tweet and isolates its text so that it can be used instead of the truncated text
        try:
            referenced_tweet_id = tweet.referenced_tweets[0].id
            referenced_tweet = clientAPI.get_tweet(id=referenced_tweet_id)
            referenced_tweet_text = referenced_tweet.data.text
            # now that we have the text from the original tweet, we replace the retweet's text with the original tweet's text
            trimmed_text = str(text)
            trimmed_text = trimmed_text.split(':')[0]
            fixed_text = trimmed_text + ": " + referenced_tweet_text
        except AttributeError:
            pass
        except TypeError:
            pass
        tweets_formatted = [tweet_id, created_at, user.data.location, user.data.username, fixed_text]


        # code to only pull tweets from georgia
        # THIS SHOULD BE ONLY BE USED IF YOU WANT TO FILTER BASED ON USER LOCATION
        user_location_str = str(user.data.location).upper()
        #if re.search(georgia_regex, user_location_str) == True:

        df.loc[len(df)] = tweets_formatted
        
        #print(tweets_formatted)
        #print(fixed_text)
        #print('------')
    return df

# this is the query for which we will use to filter our tweets
# UPDATE THIS BEFORE RUNNING SCRIPT - GOOD QUERIES BELOW
# Georgia Senate
# GA Senate
# #GeorgiaSenate
# #GASenate
# Georgia Senate Race
# GA Senate Race
# Georgia Senate Election
# GA Senate Election
# Georgia Senate 2022
# GA Senate 2022
# Abortion, Gun, Inflation, Healthcare, Crime, Trump, Biden, Community, Family
query_txt = "Georgia Senate"

# this is where we get today's date for use in the file name
today_date = datetime.datetime.today()
today_date = today_date.strftime('%m-%d-%H-%M')

# more formatting for the file name
file_query_txt_list = query_txt.split()
file_query_txt = ""
for word in file_query_txt_list:
    file_query_txt =  file_query_txt + word + "-"

# calling the API
tweet_df = auth(query_txt)

#print(tweet_df)
#tweet_df.to_csv(r'UDA_Project_2_Prelim/tweets_folder/georgiaElection_9_28.csv')

# converting the dataframe of tweets into a CSV file
tweet_df.to_csv(r'UDA_Project_2_Prelim/tweets_folder/'+file_query_txt+today_date+'.csv')


