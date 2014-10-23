from requests_oauthlib import OAuth1Session
from flask import Flask, request, redirect, session, url_for
from flask import make_response
from flask import render_template
from flask.json import jsonify
import os

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
client_id = keys.apikey
client_secret = keys.apisecret

app = Flask(__name__)

request_url = "https://www.flickr.com/services/oauth/request_token"
authorization_base_url = "https://www.flickr.com/services/oauth/authorize"
token_url = "https://www.flickr.com/services/oauth/access_token"

@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Flickr)
    using an URL with a few key OAuth parameters.
    """
    """
    Step 0? Check if user is logged into Flickr and is authenticated
    Look up logged in Flickr user in the DB/session/textfile?
    """
    #from flickrAPI import FlickrAPI
    #flickr = FlickrAPI()
    #info = flickr.test_login() # requires authentication with 'read' permissions
    #return str(info)

    if request.cookies.get('oauth_token'):
        # we'll try an authenticated call, to see if the token has been revoked or not
        from flickrAPI import FlickrAPI
        flickr = FlickrAPI(key=request.cookies.get('oauth_token'), secret=request.cookies.get('oauth_token_secret'))
        info = flickr.test_login() # requires authentication with 'read' permissions

        if info['stat'] == 'ok':
            return redirect(url_for('.profile'))
        else:
            # go and reauthenticate
            pass

    #flickr = OAuth1Session(keys.apikey, client_secret=keys.apisecret, callback_uri="http://127.0.0.1:5000/callback")
    flickr = OAuth1Session(keys.apikey, client_secret=keys.apisecret, callback_uri="http://ciaron.net/favr/callback")
    fetch_response = flickr.fetch_request_token(request_url)
    session['resource_owner_key'] = fetch_response.get('oauth_token')
    session['resource_owner_secret'] = fetch_response.get('oauth_token_secret')
    authorization_url = flickr.authorization_url(authorization_base_url, perms="read")

    return redirect(authorization_url)

# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    from urlparse import parse_qs
    verifier = parse_qs(request.url)['oauth_verifier']

    flickr = OAuth1Session(keys.apikey,
                           client_secret=keys.apisecret,
                           resource_owner_key=session['resource_owner_key'],
                           resource_owner_secret=session['resource_owner_secret'],
                           verifier=verifier)

    flickr.parse_authorization_response(request.url)
    oauth_tokens = flickr.fetch_access_token(token_url)
    """
    oauth_tokens == (e.g.)
    {u'fullname': u'Ciaron Linstead',
     u'oauth_token': u'72157648866112821-318db3245644fdf5',
     u'oauth_token_secret': u'b0d01b6ad83631c3',
     u'user_nsid': u'44124394781@N01',
     u'username': u'ciaron'}
    """
    #resp = make_response(render_template('authorised.html'))
    resp = make_response(redirect(url_for('.profile')))

    # save the tokens/info in a cookie
    resp.set_cookie('user_nsid', oauth_tokens.get('user_nsid'))
    resp.set_cookie('oauth_token', oauth_tokens.get('oauth_token'))
    resp.set_cookie('oauth_token_secret', oauth_tokens.get('oauth_token_secret'))
    resp.set_cookie('username', oauth_tokens.get('username'))

    return resp
    #return redirect(url_for('.profile'))

@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth1 token.
    """
    from flickrAPI import FlickrAPI
    #flickr = FlickrAPI(key=session['resource_owner_key'], secret=session['resource_owner_secret'])
    flickr = FlickrAPI(key=request.cookies.get('oauth_token'), secret=request.cookies.get('oauth_token_secret'))
    faves = flickr.favorites_getList(user_id="44124394781@N01", page=1, per_page=5, extras='owner_name')
    return str(faves)

if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True)
