from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flickrAPI import FlickrAPI

app = Flask(__name__)
flickr = FlickrAPI()

@app.route('/')
def index():
    return 'welcome to favr3!'

@app.route('/user/')
@app.route('/user/<user_id>')
def faves(user_id=None):
    """ show faves for user=<user_id>
    """
    faves = flickr.favorites_getList(user_id=flickr.user_id, page=1, per_page=20)
    
    return render_template('faves.html', user_id=user_id, faves=faves)

if __name__ == '__main__':
    Bootstrap(app)
    app.run(debug=True)
