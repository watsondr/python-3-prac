# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 21:19:39 2019

@author: campb
"""

from dateutil.parser import parse
from collections import Counter
import json, requests


"""
INTRO TO API BEGIN

# json needs to be serailized into a string format via encapsulation
# below simulates a JSON response
# for XML use beautifulSoup
# SEE PAGE 115 DATA SCIENCE FROM SCRATCH FOR CORRECT seralised JSON example INPUT
serialised = { "title" : "Data Science Book",
                  "author" : "Campbell Sinclair",
                  "publicationYear" : 2014,
                  "topics" : [ "data", "science", "data science" ] }

# parse JSON to create a python dict
deserialised = json.loads(serialised)

if "data science" in deserialised["topics"]:
   print(deserialised["topics"])
   
INTRO TO API END
"""

"""
INTRO TO UNAUTHENTICATED API
"""

endpoint = "https://api.github.com/users/watsondr/repos"

repos = json.loads(requests.get(endpoint).text)

dates = [parse(repo["created_at"]) for repo in repos]
# not_parsed = [repo["created_at"] for repo in repos]

month_counts = Counter(date.month for date in dates)
weekday_counts = Counter(date.weekday() for date in dates)

last_repos = sorted(repos,
                    key=lambda r: r["created_at"],
                    reverse=True)[:3]

last_languages = [repo["language"] for repo in last_repos]


