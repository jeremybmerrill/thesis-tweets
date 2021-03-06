import tweetstream
from tweetvizconfig import twitter_username, hashtags as config_hashtags, initial_users_to_follow, modules
from time import mktime, gmtime, localtime, asctime
import codecs

class Tweetviz:
  my_modules = []
  username = twitter_username
  password = ""
  users_to_follow = []
  hashtags = config_hashtags
  old_html = dict();
  time = 0
  start_time = 0

  def __init__(self):
    self.users_to_follow = initial_users_to_follow

    self.password = raw_input("Twitter password:\n")


    for module_name in modules:
      module = __import__(module_name)
      module_class_name = module_name.title()
      self.my_modules.append(getattr(module, module_class_name)())


  def start(self):
      with tweetstream.FilterStream(self.username, self.password, track=self.hashtags,
                                      follow=self.users_to_follow) as stream:
        self.start_time = localtime() #TODO Note the start time.
        restart_asap = False
        for tweet in stream:
          if tweet and tweet.get("text", False):
            #print tweet["text"]
            #send tweets to modules.
            for module in self.my_modules:
              module_return = module.use_tweet(tweet)
              #print module.name() + " using " + tweet["text"]

              if "users" in module_return:
                self.users_to_follow.extend(module_return["users"])
              restart_asap = module_return.get("restart", False)
            if(mktime(gmtime()) % 300 == 0) and self.time != mktime(gmtime()): #every five minutes, get a new trending topics
              self.time = mktime(gmtime())
              self.getHTML()
            else:
              #print "Received tweet: " + tweet["text"]
              pass
            if restart_asap:
              break #TODO: (check if this really just boosts us out to a new tweetstream.Filterstream thing.
              self.start() #will it work for restarting the loop (with new users to track or whatever) to just do this?

            #TODO: Check if loop hasn't been restarted in a while, if not, restart (including new users to track, or whatever.)

  def dealWithHTML(self, html):
      if "trending" in html:
        filename = "trending.html"
      elif "yourguys" in html:
        filename = "yourguys.html"
      with codecs.open(filename, mode="w", encoding="utf-8") as f:
            f.write("<html>\n<head>\n<title>Tweetviz</title>\n</head>\n<body>")
            f.write("<span class='starttime'>" + asctime(self.start_time) + "</span>")
            f.write("<span class='updatetime'>" + asctime(localtime()) + "</span>")
            f.write(unicode(html))
            f.write("</body>\n</html>")
      print("Updating " + filename + " at " + asctime(localtime()))
        

  def getHTML(self):
    returnstring = ""
    for module in self.my_modules:
      self.dealWithHTML(module.get_viz()) 




#Thought: have a "backstop" loop that records tweets and sends them to the tweetviz object after it restarts
