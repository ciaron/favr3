#import oauth2 as oauth
from requests_oauthlib import OAuth1Session

#import time
#import httplib2
#import urlparse

class APIKeys:
    """Helper class to read the API Keys"""
    def __init__(self,filename):
        if filename is None:
            raise ValueError("No File Specified")
        self.filename = filename
        try:
            fp = open("apikeys")
        except IOError as e:
            if e.errno == errno.EACCESS:
                print "file does not exists"
            # Not a permission error.
            raise 
        else:
            with fp:
                self.apikey = fp.readline().rstrip('\n')
                self.apisecret = fp.readline().rstrip('\n')
                fp.close()

# Read the APIKeys
keys = APIKeys("apikeys")
print keys.apikey
print keys.apisecret

# OAuth authentication based on requests-oauthlib
# See: http://requests-oauthlib.readthedocs.org/en/latest/oauth1_workflow.html

# Set the API endpoint 
request_url = "https://www.flickr.com/services/oauth/request_token"
base_authorization_url = "https://www.flickr.com/services/oauth/authorize"
access_token_url = "https://www.flickr.com/services/oauth/access_token"

# step 1: obtain a request token to identify self at next step
oauth = OAuth1Session(keys.apikey, client_secret=keys.apisecret, callback_uri="http://ciaron.net")
fetch_response = oauth.fetch_request_token(request_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

# step 2: obtain autorization from the user
authorization_url = oauth.authorization_url(base_authorization_url)
print 'Please go here and authorize,', authorization_url
redirect_response = raw_input('Paste the full redirect URL here: ')
oauth_response = oauth.parse_authorization_response(redirect_response)
verifier = oauth_response.get('oauth_verifier')

# step 3: obtain an access token from the OAuth provider
oauth = OAuth1Session(keys.apikey,
                      client_secret=keys.apisecret,
                      resource_owner_key=resource_owner_key,
                      resource_owner_secret=resource_owner_secret,
                      verifier=verifier)

oauth_tokens = oauth.fetch_access_token(access_token_url)

resource_owner_key = oauth_tokens.get('oauth_token')
resource_owner_secret = oauth_tokens.get('oauth_token_secret')

##write out a file with the oauth_token and oauth_token_secret (resource_owner_key/secret)
with open('token', 'w') as f:
    f.write(resource_owner_key + '\n')
    f.write(resource_owner_secret)
f.closed

