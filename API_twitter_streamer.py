# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 20:29:01 2020

@author: campb
"""

from twython import TwythonStreamer
import json

# "w" instead of "r" and dump instead of load for vice-versa file interaction
with open("credentials.json", "r") as read_file:
    credentials_data = json.load(read_file)
    
CONSUMER_KEY = credentials_data["twitter"]["consumer_key"]
CONSUMER_SECRET = credentials_data["twitter"]["consumer_secret"];
ACCESS_TOKEN = credentials_data["twitter"]["access_token"]
ACCESS_SECRET = credentials_data["twitter"]["access_secret"];


tweets = []

class MyStreamer(TwythonStreamer):
    """ THIS DEFINES HOW WE INTERACT WITH TWITTER DATA !!
        IRL:
            You would want to add these tweets to a data store
            Not unsecure global variables in memory
    """
    
    def on_success(self, data):
        """ transfer Twitter payload to Python dict """
        5.
        # only care about tweets we can actually read
        if 'lang' in data:
            if data['lang'] == 'en':
                tweets.append(data)
                print("received tweet #: {}".format(len(tweets)))
                  
        # stop when we have enough data points
        if len(tweets) >= 1000:
            print(tweets)
            self.disconnect()
        
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
# track below looks for keyword. replace filter() with sample() for any public tweet?!
stream.statuses.filter(track='#australiafire')

""" 

find the most popular hastags example 

top_hashtags = Counter(hashtag['text'].lower()
                        for tweet in tweets
                        for hashtag in tweet["entities]["hashtags"])
print(top_hashtags.most_common(5))


"""