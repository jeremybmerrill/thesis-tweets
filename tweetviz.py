import tweetstream
from tweetvizconfig import twitter_username, hashtags, initial_users_to_follow, modules

class Tweetviz:
  my_modules = []
  username = twitter_username
  password = ""
  users_to_follow = []
  hashtags

  def __init__(self):
    self.users_to_follow = initial_users_to_follow

    self.password = raw_input("Twitter password:\n")


    for module in modules:
      __import__(module)
      module_class_name = module.title()
      self.my_modules.append(getattr(module, module_class_name)())


  def start(self):
      with tweetstream.FilterStream(self.username, self.password, track=self.hashtags,
                                    follow=self.users_to_follow) as stream:
        start_time = 0 #TODO Note the start time.
        restart_asap = False
        for tweet in stream:
          #send tweets to modules.
          for module in self.my_modules:
            module_return = module.use_tweet(tweet)
            print module.name() + " using " + tweet["text"]

            if "users" in module_return:
              self.users_to_follow.extend(module_return["users"])
            restart_asap = module_return.get("restart", False)

          if restart_asap:
            break #TODO: (check if this really just boosts us out to a new tweetstream.Filterstream thing.
            self.start() #will it work for restarting the loop (with new users to track or whatever) to just do this?


          #TODO: Check if loop hasn't been restarted in a while, if not, restart (including new users to track, or whatever.)


#Thought: have a "backstop" loop that records tweets and sends them to the tweetviz object after it restarts
