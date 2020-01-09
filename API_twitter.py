# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 01:01:23 2020

@author: campb
"""

from twython import Twython
import json

# "w" instead of "r" and dump instead of load for vice-versa file interaction
with open("credentials.json", "r") as read_file:
    credentials_data = json.load(read_file)
    
CONSUMER_KEY = credentials_data["twitter"]["consumer_key"]
CONSUMER_SECRET = credentials_data["twitter"]["consumer_secret"];

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET)

# search for tweets containing a phrase
for status in twitter.search(q='"#AustraliaBurning"')["statuses"]:
    user = status["user"]["screen_name"].encode('utf-8').decode('utf-8')
    text = status["text"].encode('utf-8').decode('utf-8')
    print(user, ":", text)
    print()
    
