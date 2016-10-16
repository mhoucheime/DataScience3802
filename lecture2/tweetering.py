""" Streaming twitter API example """

from __future__ import print_function
import sys
import tweepy
from ConfigParser import ConfigParser

class TwitterListener(tweepy.StreamListener):
    """ Twitter stream listener. """

    def __init__(self,filename,nooflines):
        print ('Twitter Listener constructed')
	super(TwitterListener, self).__init__()
	self.filename = filename
	self.file =  open("data/"+filename, 'w')
	self.nolines = nooflines
	self.line = 0

    def on_status(self, tweet):
	print ("Receiving tweet no :"+str(self.line))
	if self.line < int(self.nolines):
	   self.file.write(tweet.text.encode('ascii','ignore'))
           self.line = self.line + 1
	else :
	   self.file.close()
	   exit()

    def on_error(self, msg):
        print('Error: %s', msg)

    def on_timeout(self):
        print('timeout : wait for next poll')
        sleep(10)

def get_config():
    """ Get the configuration """
    conf = ConfigParser()
    conf.read('../cfg/mona.cfg')
    return conf

def get_stream(filepath,no_of_lines):
    config = get_config()
    auth = tweepy.OAuthHandler(config.get('twitter', 'consumer_key'),
                               config.get('twitter', 'consumer_secret'))

    auth.set_access_token(config.get('twitter', 'access_token'),
                          config.get('twitter', 'access_token_secret'))

    listener = TwitterListener(filepath,no_of_lines)
    stream = tweepy.Stream(auth=auth, listener=listener)
    return stream

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: %s <word> <no_of_lines> <filepath>" % (sys.argv[0]))
    else:
        word = sys.argv[1]
	no_of_lines = sys.argv[2]
	filepath = sys.argv[3]
        stream = get_stream(filepath,no_of_lines)
        print("Listening to '%s' and '%s' ..." %('#' + word, word))
        stream.filter(track=['#' + word, word])
