from tweetvizmodule import Tweetvizmodule
from time import *
from math import log
from tweetvizutils import clean

#TODO: clear dictionaries when they get too big.
#TODO: normalize for capitalization

class Tweetviztrending(Tweetvizmodule):
  name = "TweetvizTrending"

  unigrams = dict() #dict mapping terms to total frequencies over corpus.
  bigrams = dict()
  word_count = 0
  less_recent_unigrams = dict()
  less_recent_bigrams = dict()
  recent_unigrams = dict()
  recent_bigrams = dict()
  update_time = 0
  num_docs = 0


  def __init__(self):
    # should this "seed" data. (Perhaps with results of zipfs law, so we don't get "the" as a trending topic at first.)
    # Update: It looks like that's not necessary, results are decent without it.
    update_time = mktime(gmtime())

  def use_tweet(self, tweet):
    tweet_words = clean(tweet["text"]).split()
    self.word_count += len(tweet_words)
    
    prev_word = None
    for upword in tweet_words:
      word = upword.lower()
      self.unigrams[word] = self.unigrams.get(word, 0.0) + 1.0
      self.recent_unigrams[word] = self.recent_unigrams.get(word, 0.0) + 1.0

      if prev_word:
        bigram = ' '.join([prev_word, word])
        self.bigrams[bigram] = self.bigrams.get(bigram, 0.0) + 1.0
        self.recent_bigrams[bigram] = self.recent_bigrams.get(bigram, 0.0) + 1.0
      prev_word = word
    self.refresh_if_necessary()
    return {'success': True}

  def refresh_if_necessary(self):
    """ If dicts are too big or it's been a while, refresh.
  
        Refreshing moves the current recent_<n>grams to less_recent_<n>grams and clears recent_<n>grams.
    """ 
    if mktime(gmtime()) - self.update_time > 300 or len(self.recent_bigrams) > 10000: #refresh every five minutes
      #print len(self.recent_bigrams)
      self.refresh()
    else:
      pass


  def refresh(self):
    #x = raw_input("Press Enter:" )
    self.less_recent_unigrams = self.recent_unigrams
    self.less_recent_bigrams = self.recent_bigrams
    self.recent_bigrams = dict()
    self.recent_unigrams = dict()
    self.update_time = mktime(gmtime())
    self.num_docs += 1

  def get_trends(self):
    """ Return the uni/bigrams with the highest frequencies relative to all collected ngrams.
  
      Note that we throw out any ngrams with total tokens < 10. These are too uncommon to be trending.
    """
    all_ngram_ratios_list = []
    for ngrams, recent_ngrams in ((self.unigrams, self.recent_unigrams), (self.bigrams, self.recent_bigrams)):
      ngram_ratios = dict()
      for ngram, recent_freq in recent_ngrams.iteritems():
        if ngrams.get(ngram, 0) > 10: #only consider ngrams with a total count greater than 10 as possible trends
          ngram_ratios[ngram] = recent_freq * self.num_docs / ngrams[ngram] #proper TFIDF would require a log() here. But that gives poor results. Hence, no log.
      all_ngram_ratios_list.append(ngram_ratios)
    
    all_ngram_ratios = {}
    for ratio_dict in all_ngram_ratios_list:
        for key, val in ratio_dict.items():
            all_ngram_ratios[key] = val
    
    sorted_ngrams = sorted(all_ngram_ratios, key=lambda x: all_ngram_ratios[x])
    sorted_ngrams = filter(lambda x: all_ngram_ratios[x] != 1.0, sorted_ngrams) # if an item has a ratio of 1, then all of its tokens have occurred in the last pass-through. It might be trending, or it might just be rare. If it's actually trending, we'll catch it next time.
    #print "lowest ratio new:log(total)"
    #for ngram in sorted_ngrams[:10]:
    #    print ngram + " " + str(all_ngram_ratios[ngram])
    #print "highest ratio new:log(total)"
    #for ngram in sorted_ngrams[-10:]:
    #    print ngram + " " + str(all_ngram_ratios[ngram])
    trending_topics = sorted_ngrams[-10:]
    trending_topics.reverse()
    return trending_topics

  def format_trends(self, trends):
    html_list_to_return = []
    html_list_to_return.append('<span class="tweetviz-trending-metadata">Total unigrams: ' + str(len(self.unigrams)) + ", Total bigrams: " + str(len(self.bigrams))  + '</span>')
    html_list_to_return.append('<span class="tweetviz-trending-metadata">Recent unigrams: ' + str(len(self.recent_unigrams)) + ", Recent bigrams: " + str(len(self.recent_bigrams))  + '</span>')
    html_list_to_return.append('<ul class="tweetviz-trending">')
    for trend in trends:
      my_html_list = ['<li class="tweetviz-trending-trend">']
      #lmy_html_list.append('<a href="http://twitter.com/search?q=' + trend + '">') #fix search query.
      my_html_list.append("<a>")
      my_html_list.append(trend)
      my_html_list.append('</a></li>')
      html_list_to_return.append(''.join(my_html_list))
    html_list_to_return.append( "</ul>")
    return '\n'.join(html_list_to_return)

  def get_viz(self):
    return self.format_trends(self.get_trends())

