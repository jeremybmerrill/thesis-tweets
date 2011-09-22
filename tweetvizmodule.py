class Tweetvizmodule:
  #"abstract" class of modules.
  name = ""

  def __init__(self):
    pass

  def name(self):
    return name

  def use_tweet(self, tweet):
    """ Returns a dict containing message to be sent to tweetviz object.

        E.g. dict("users":"jeremybmerrill") will tell the tweetviz object to start following user jeremybmerrill on next restart, 
        dict("restart": True) tells the tweetviz object to restart ASAP.
    """
    
    raise NotImplementedError
    return dict()

  def get_viz(self):
    """Return the HTML formatted (as some block element) interesting displayable result of the module."""
    raise NotImplementedError
