from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap
from flickrAPI import FlickrAPI

app = Flask(__name__)

@app.route('/')
def index():
    return 'welcome to favr3!'

@app.route('/user/')
@app.route('/user/<user_id>')
def faves(user_id=None, page=1):
    """ show faves for user=<user_id>
    """
    try: 
        page = request.args.get('page')
    except:
        pass

    flickr = FlickrAPI(key=request.cookies.get('oauth_token'), secret=request.cookies.get('oauth_token_secret'))

    if user_id == None:
        # TODO get the logged-in user's ID
        user_id = flickr.user_id

    username = flickr.people_getInfo(user_id=user_id)
    if username['stat'] == 'ok':
    
        faves = flickr.favorites_getList(user_id=user_id, page=page, per_page=12, extras='owner_name')
        return render_template('faves.html', user_id=user_id, faves=faves, username=username['person']['username']['_content'])
    else:
        return str(username)

if __name__ == '__main__':
    Bootstrap(app)
    app.run(debug=True)
