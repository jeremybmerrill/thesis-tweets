from tweetvizmodule import Tweetvizmodule

#TODO: clear dictionaries when they get too big.

class Tweetviztrending(Tweetvizmodule):
  name = "Tweetviz Trending"

  unigrams = dict() #dict mapping terms to total frequencies over corpus.
  bigrams = dict()
  word_count = 0
  recent_unigrams = dict()
  recent_bigrams = dict()
  update_time


  def __init__(self):
    #TODO "seed" data. (Perhaps with results of zipfs law, so we don't get "the" as a trending topic at first.)
    pass

  def use_tweet(self, tweet):
    tweet_words = tweet["text"].split()
    word_count += len(tweet_words)
    
    prev_word
    for word in tweet_words:
      if word in self.unigrams:
        self.unigrams[word] += 1
      else:
        self.unigrams[word] = 1
      
      bigram = ' '.join([prev_word, word])
      if bigram in self.bigrams:
        self.bigrams[bigram] += 1
      else:
        self.bigrams[bigram] = 1

      if word in self.recent_unigrams:
        self.recent_unigrams[word] += 1
      else:
        self.recent_unigrams[word] = 1
      
      bigram = ' '.join([prev_word, word])
      if bigram in self.recent_bigrams:
        self.recent_bigrams[bigram] += 1
      else:
        self.recent_bigrams[bigram] = 1
      
      prev_word = word

  def refresh_if_necessary(self):
    if self.update_time 


  def get_trends(self):
    """ Return the uni/bigrams with the highest frequencies relative to all collected ngrams."""
    all_ngram_ratios = dict()
    for ngrams, recent_ngrams in ((self.unigrams, self.recent_unigrams), (self.bigrams, self.recent_bigrams)):
      ngram_ratios = dict()
      for ngram, recent_freq in recent_ngrams.iteritems():
        ngram_ratios[ngram] = recent_freq / ngrams.get(ngram, 1000) #if it isn't it the total ngrams, something went wrong, but this isn't a trending ngram
      all_ngram_ratios.add(ngram_ratios) #TODO: mush the dicts together.
    
    sorted_ngrams = sorted([(val, key) for key, val in all_ngram_ratios.iteritems()])
    return sorted_ngrams.values()[:10]

  def format_trends(trends):
    html_list_to_return = ['<ul class="tweetviz-trending">']
    for trend in trends:
      my_html_list = ['<li class="tweetviz-trending-trend>']
      my_html_list.append('<a href="http://twitter.com/search?q=' + trend + '">') #fix search query.
      my_html_list.append(trend)
      my_html_list.append('</a></li>')
    
    html_list_to_return.append( "<ul>")
    return ''.join(html_list_to_return)

  def get_viz(self):
    return self.format_trends(self.get_trends())

        
        

    
