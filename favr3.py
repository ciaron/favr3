import os
from flask import Flask
from flask import render_template
from flask import request, redirect, session
from flask import make_response
from flask import url_for
from flask_bootstrap import Bootstrap
from requests_oauthlib import OAuth1Session

from flickrKeys import APIKeys
from flickrAPI import FlickrAPI

request_url = "https://www.flickr.com/services/oauth/request_token"
authorization_base_url = "https://www.flickr.com/services/oauth/authorize"
token_url = "https://www.flickr.com/services/oauth/access_token"

# Read the APIKeys
keys = APIKeys("apikeys")
client_id = keys.apikey
client_secret = keys.apisecret

app = Flask(__name__)

@app.route('/auth')
def auth():
    flickr = OAuth1Session(keys.apikey, client_secret=keys.apisecret, callback_uri="http://127.0.0.1:5000/callback")
    fetch_response = flickr.fetch_request_token(request_url)
    session['resource_owner_key'] = fetch_response.get('oauth_token')
    session['resource_owner_secret'] = fetch_response.get('oauth_token_secret')
    authorization_url = flickr.authorization_url(authorization_base_url, perms="read")
    return redirect(authorization_url)

@app.route('/public/', methods=['GET', 'POST'])
@app.route('/public/<user_id>', methods=['GET', 'POST'])
def publicfaves(user_id=None, page=1):
    flickr = FlickrAPI()

    username = None

    if request.method == 'POST':
        #return "not implemented yet"
        flickr = FlickrAPI()
        name = str(request.form["name"])
        # name is either an NSID or username
        r = flickr.people_getInfo(user_id=name)

        if r['stat'] == 'fail':
            # probably wasn't an NSID, try it as a username
            r = flickr.people_findByUsername(username=name)
            if r['stat'] == 'fail':
                pass # dunno?
                return "no user found"
            else:
                username = name
                user_id = r['user']['nsid']
        else:
            # use username below
            username = r['person']['username']['_content']
            user_id = name
        #return str({'username': username, 'user_id':user_id})

    if not user_id:
        user_id = flickr.user_id
    r = flickr.people_getInfo(user_id=user_id)
    username = r['person']['username']['_content']

    try: 
        page = request.args.get('page')
    except:
        pass

    if r['stat'] == 'ok':
        publicfaves = flickr.favorites_getPublicList(user_id=user_id, page=page, per_page=12, extras='owner_name')
        return render_template('faves.html', user_id=user_id, faves=publicfaves, username=username, public=True)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<user_id>', methods=['GET', 'POST'])
def faves(user_id=None, page=1):
    """ show faves for user=<user_id>
    """

    username = None

    if request.method == 'POST':
        #return "not implemented yet"
        flickr = FlickrAPI()
        name = str(request.form["name"])
        # name is either an NSID or username
        r = flickr.people_getInfo(user_id=name)

        if r['stat'] == 'fail':
            # probably wasn't an NSID, try it as a username
            r = flickr.people_findByUsername(username=name)
            if r['stat'] == 'fail':
                pass # dunno?
                return "no user found"
            else:
                username = name
                user_id = r['user']['nsid']
        else:
            # use username below
            username = r['person']['username']['_content']
            user_id = name
        #return str({'username': username, 'user_id':user_id})

    if not request.cookies.get('oauth_token'):
        #print "NOT AUTHORISED"
        return render_template('choice.html')        
        #return redirect(url_for('auth'))

    else:
        #print "AUTHORISED"
        # we'll try an authenticated call, to see if the token has been revoked or not
        flickr = FlickrAPI(key=request.cookies.get('oauth_token'), secret=request.cookies.get('oauth_token_secret'))
        info = flickr.test_login() # requires authentication with 'read' permissions

        if info['stat'] == 'ok':
            #return redirect(url_for('faves'))
            pass
        else:
            # go and reauthenticate
            return redirect(url_for('auth'))

        # we're authorised, go ahead.
        try: 
            page = request.args.get('page')
        except:
            pass

        flickr = FlickrAPI(key=request.cookies.get('oauth_token'), secret=request.cookies.get('oauth_token_secret'))

        if user_id == None:
            # TODO get the logged-in user's ID
            user_id = flickr.user_id
            #print "HERE"

        if not username:
            r = flickr.people_getInfo(user_id=user_id)
            if r['stat'] == 'fail':
                return "no username!"
            else:
                username = r['person']['username']['_content']
    
        faves = flickr.favorites_getList(user_id=user_id, page=page, per_page=12, extras='owner_name')
        return render_template('faves.html', user_id=user_id, faves=faves, username=username, public=False)

    return "FAIL"

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
    resp = make_response(redirect(url_for('faves')))

    # save the tokens/info in a cookie
    resp.set_cookie('user_nsid', oauth_tokens.get('user_nsid'))
    resp.set_cookie('oauth_token', oauth_tokens.get('oauth_token'))
    resp.set_cookie('oauth_token_secret', oauth_tokens.get('oauth_token_secret'))
    resp.set_cookie('username', oauth_tokens.get('username'))

    return resp

if __name__ == '__main__':
    Bootstrap(app)
    os.environ['DEBUG'] = "1"
    app.secret_key = os.urandom(24)
    app.run(debug=True)

