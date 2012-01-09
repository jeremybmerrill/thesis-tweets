"""
A collection of utilities for use in Tweetviz modules.
Jeremy B. Merrill
12/25/11
"""

def clean(tweet):
    import re
    return re.sub("[\n\r]", " ",re.sub("[.,:!?]","", tweet))
