import config # local config, API Key, Secret etc.
#import flickrapi
import oauth2 as oauth
import time
import httplib2

# get public favorites
#faves = flickr.favorites_getPublicList(user_id=config.USER)

# get all favorites
# (requires authenticated access)
#faves = flickr.favorites_getList(user_id=config.USER)

# Code via http://mkelsey.com/2011/07/03/Flickr-oAuth-Python-Example/

url = "http://www.flickr.com/services/oauth/request_token"

params = {
    'oauth_timestamp': str(int(time.time())),
    'oauth_signature_method':"HMAC-SHA1",
    'oauth_version': "1.0",
    'oauth_callback': "http://ciaron.net",
    'oauth_nonce': oauth.generate_nonce(),
    'oauth_consumer_key': config.API_KEY,
}

# Setup the Consumer with the api_keys given by the provider
consumer = oauth.Consumer(key=config.API_KEY, secret=config.API_SECRET)

# Create our request. Change method, etc. accordingly.
req = oauth.Request(method="GET", url=url, parameters=params)

# Create the signature
signature = oauth.SignatureMethod_HMAC_SHA1().sign(req,consumer,None)

# Add the Signature to the request
req['oauth_signature'] = signature

# Make the request to get the oauth_token and the oauth_token_secret
# I had to directly use the httplib2 here, instead of the oauth library.
h = httplib2.Http(".cache")
resp, content = h.request(req.to_url(), "GET")

print resp, content
