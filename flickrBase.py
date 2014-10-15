import json
from requests_oauthlib import OAuth1Session
from flickrKeys import APIKeys, TokenKeys

class FlickrApiMethod(object):
    """Base class for Flickr API calls"""

    def __init__(self, nojsoncallback=True, format='json', parameters=None):

        # read the secrets/key from file
        apifile = APIKeys()
        tokenfile = TokenKeys()

        self.token = tokenfile.token

        self.loaded = False

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
            apifile.apikey,
            client_secret=apifile.apisecret,
            resource_owner_key=tokenfile.token,
            resource_owner_secret=tokenfile.secret
        )

        if self.makeCall():
            self.loaded = True

    def makeCall(self):
        self.parameters.update(self.getParameters())

        call_url = self.url + '?method=' + self.name

        r = self.oauth.get(call_url, params=self.parameters)

        self.content = r.content
        self.json = json.loads(r.content)

        if self.json["stat"] == "ok":
            return True
        else:
            return False

    def getParameters(self):
        raise NotImplementedError
