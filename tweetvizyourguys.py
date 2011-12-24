from tweetvizmodule import Tweetvizmodule

#TODO: clear dictionaries when they get too big.

"""
What's my goal here?
Use API to gather tokens of "your guys NOUN", "your folks NOUN" "your twos NOUN", etc.
1. Count "your guys NOUN", folks, twos, threes
    Do I want to count tweets or following nouns? I don't give a shit about the following nouns, I just want the tweets.
2. Count you guys versus y'all versus you all versus youse guys. (Age?)

I need two modules -- one for each purpose
"""

class Tweetvizyourguys(Tweetvizmodule):
  name = "Tweetviz Guys"

  yourguys = [] #whatever three words comes after "your guys" -- later, checked to see if it's a noun, for a double-possessive phenomenon.
  yourfolks = []
  yourtwos = []
  yourthrees = []
  update_time = 0

  tokens = {"your guys": yourguys, "your folks": yourfolks, "your twos":yourtwos, "your threes":yourthrees} #what this module cares about.

  def __init__(self):
    #TODO "seed" data. (Perhaps with results of zipfs law, so we don't get "the" as a trending topic at first.)
    pass

  def use_tweet(self, tweet):
    #tweet does not necessarily contains an instance of what we care about in this module.
    for token in self.tokens.keys():
      if token in tweet:
        self.increment_dict(tweet, token)

  def increment_dict(tweet, token):
    tweet_after_token = tweet.split(token)[1]
    if tweet_after_token[0] == "'": #if it's "your guys' X"
      self.tokens[token].append(tweet)
    else:
      pass #right now, I'm only counting "your guys'" tokens. 
        #How will I distinguish "Be careful to make sure your guys don't get tired" and "I want to read your guys DMs"     
        #Should I have two sets of dicts for those that I think are most likely to be relevant tweets and those that aren't? 
        #Should I check for verbs or nouns following the token? (and throw out the ones where the first verb precedes the first noun.
    
  def refresh_if_necessary(self):
    pass

  def flush(self):
    #write to file?
    print yourguys



        
        

    
