import json
import functools
from requests_oauthlib import OAuth1Session
from flickrKeys import APIKeys, TokenKeys

class FlickrAPI(object):

    def __init__(self, nojsoncallback=True, format='json', parameters=None):
        self.apifile = APIKeys()
        self.tokenfile = TokenKeys()
        self.url = "https://api.flickr.com/services/rest"

    def create(self, *args, **kwargs):
        print "args %r and kwargs %r" % (args, kwargs)

    def __getattr__(self, attrName):
        return functools.partial(self.create, attrName)

