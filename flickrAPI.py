import json
import functools
from requests_oauthlib import OAuth1Session
from flickrKeys import APIKeys, TokenKeys

class FlickrAPI(object):

    def __init__(self, nojsoncallback=True, format='json', parameters=None):
        self.user_id = '44124394781@N01' #TESTING
        self.apifile = APIKeys()
        self.tokenfile = TokenKeys()
        self.url = "https://api.flickr.com/services/rest"

        if nojsoncallback:
            self.nojsoncallback = 1
        else:
            self.nojsoncallback = 0

        if not parameters:
            parameters = {}

        self.url = "https://api.flickr.com/services/rest"

        defaults = {
            'format': format,
            'nojsoncallback': self.nojsoncallback,
        }

        defaults.update(parameters)
        self.parameters = defaults

        self.oauth = OAuth1Session(
            self.apifile.apikey,
            client_secret=self.apifile.apisecret,
            resource_owner_key=self.tokenfile.token,
            resource_owner_secret=self.tokenfile.secret
        )


    def create(self, *args, **kwargs):
        #print "args %r and kwargs %r" % (args, kwargs)

        # update the API parameters with the arguments we received:
        self.parameters.update(kwargs)

        s = 'flickr.' + args[0].replace('_', '.')
        call_url = self.url + '?method=' + s
    
        # make the authenticated call to Flickr
        r = self.oauth.get(call_url, params=self.parameters)

        self.content = r.content
        self.json = json.loads(r.content)

        return self.json

    def __getattr__(self, attrName):
        # 1. update self.parameters with attrs

        # 2. create (and call) the function

        return functools.partial(self.create, attrName)

