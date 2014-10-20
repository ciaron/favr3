import json
import functools
from requests_oauthlib import OAuth1Session
from flickrKeys import APIKeys, TokenKeys

class FlickrAPI(object):

    def __init__(self, nojsoncallback=True, format='json', parameters=None, key=None, secret=None):
        self.user_id = '44124394781@N01' #TESTING
        self.apifile = APIKeys()
        # TODO: the key and secret here are the token/auth keys! make this clear
        # TODO: add a set_keys() method?
        if key == None:
            self.tokenfile = TokenKeys()
            self.resource_owner_key=self.tokenfile.token
            self.resource_owner_secret=self.tokenfile.secret
        else:
            self.resource_owner_key=key
            self.resource_owner_secret=secret

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
            resource_owner_key=self.resource_owner_key,
            resource_owner_secret=self.resource_owner_secret
        )

    def create(self, *args, **kwargs):

        # update the API parameters with the arguments we received:
        self.parameters.update(kwargs)

        s = 'flickr.' + args[0].replace('_', '.')
        call_url = self.url + '?method=' + s
    
        # make the authenticated call to Flickr
        r = self.oauth.get(call_url, params=self.parameters)

        self.content = r.content
        #print r.content
        self.json = json.loads(r.content)

        return self.json

    def __getattr__(self, attrName):
        return functools.partial(self.create, attrName)
