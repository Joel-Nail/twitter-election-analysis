# Credit to CreepyD246 for the outline of this stream script

# Importing Tweepy and time
import tweepy
import time
import pandas as pd
import csv

# Credentials (INSERT YOUR KEYS AND TOKENS IN THE STRINGS BELOW)
api_key = ""
api_secret = ""
bearer_token = r""
access_token = ""
access_token_secret = ""

# Gainaing access and connecting to Twitter API using Credentials
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

#search_terms = ["#GeorgiaSenate", "Georgia Senate", "GA Senate", "bio_location:GA"]
#search_terms = ["bio_location:GA AND #GeorgiaSenate"]

df = pd.DataFrame(columns=['tweetID', 'created_at', 'location', 'username', 'fixedText'])

# Bot searches for tweets containing certain keywords
class MyStream(tweepy.StreamingClient):

    # This function gets called when the stream is working
    def on_connect(self):

        print("Connected")
        print("---")


    # This function gets called when a tweet passes the stream
    def on_tweet(self, tweet):

        tweet_id = tweet.id
        created_at = tweet.created_at
        author = tweet.author_id
        user = client.get_user(id=author, user_fields='location')
        text = tweet.text
        fixed_text = tweet.text

        # Displaying tweet in console
        print(tweet.text)
        print(user.data.location)
        print("---")
        # Delay between tweets
        time.sleep(0.5)

        if "RT @ReverendWarnock:" in tweet.text:
            pass
        else:

            # whenever a tweet is retweeted, twitter automatically truncates the tweet's text which we don't really want
            # the following code finds the original tweet and isolates its text so that it can be used instead of the truncated text
            try:
                referenced_tweet_id = tweet.referenced_tweets[0].id
                referenced_tweet = client.get_tweet(id=referenced_tweet_id)
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
            df.loc[len(df)] = tweets_formatted

            #TODO add code that writes tweets_formatted to stream_tweets.csv
            file = open('/Users/joelnail/Documents/UDA/UDA_Project_2_Prelim/tweepy-stream-api-v2-main/stream_tweets/stream_tweets.csv', 
                        'a', newline='')
            writer = csv.writer(file)
            writer.writerow(tweets_formatted)
            #print(len(file))
            file.close()

            
            # Displaying tweet in console
            #if tweet.referenced_tweets == None:
                #print(tweet.text)
                #client.like(tweet.id)

                # Delay between tweets
                #time.sleep(0.5)
    
    def on_disconnect(self):
        print("Disconnected")
        

# Creating Stream object
stream = MyStream(bearer_token=bearer_token)

# Adding terms to search rules
# It's important to know that these rules don't get deleted when you stop the
# program, so you'd need to use stream.get_rules() and stream.delete_rules()
# to change them, or you can use the optional parameter to stream.add_rules()
# called dry_run (set it to True, and the rules will get deleted after the bot
# stopped running).
#for term in search_terms:
#    stream.add_rules(tweepy.StreamRule(term))

# added already: #GeorgiaSenate:GA, Georgia Senate:GA, Georgia Senate:Georgia, #GeorgiaSenate:Georgia,
#                 GA Senate:GA, GA Senate:Georgia, #GASenate:GA, #GASenate:Georgia

#stream.add_rules(tweepy.StreamRule("#GeorgiaSenate bio_location:Georgia"))
#stream.add_rules(tweepy.StreamRule("GA Senate bio_location:Georgia"))
#stream.add_rules(tweepy.StreamRule("GA Senate bio_location:GA"))
#stream.add_rules(tweepy.StreamRule("#GASenate bio_location:Georgia"))
#stream.add_rules(tweepy.StreamRule("#GASenate bio_location:GA"))
#stream.add_rules(tweepy.StreamRule("Georgia Senate -'RT @ReverendWarnock:'"))
#stream.add_rules(tweepy.StreamRule("(Georgia Senate OR GA Senate OR #GeorgiaSenate OR #GASenate) (bio_location:GA OR bio_location:Georgia)"))



#stream.delete_rules(['1579482203536478209', "1579482562723979271", "1579490971905048576", "1579513196565626880", 
#                        "1579513201418444801", "1579513208259448832", "1579513218581643265", "1579513223283462145",
#                        "1579558058916810752"])

stream.add_rules(tweepy.StreamRule("(Georgia Senate OR GA Senate OR #GeorgiaSenate OR #GASenate) (bio_location:\", GA\" OR bio_location:\", Georgia\")"))

print(stream.get_rules())

#stream.add_rules(tweepy.StreamRule(tag=["bio_location:GA"]))

# Starting stream
stream.filter(tweet_fields=["referenced_tweets", "created_at", "author_id"], user_fields=["location"])

#stream.disconnect()
