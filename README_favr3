import flickrFaves
import flickrPeople
from flickrCheckToken import FlickrAuthOAuthCheckToken

q=FlickrAuthOAuthCheckToken()

if q.json['stat'] == 'ok':
    user_id = q.json['oauth']['user']['nsid']
else:
    exit()

q=flickrFaves.FlickrFavoritesGetList(user_id=user_id)

if q.json['stat'] == 'ok':
    print q.json['photos']['total']
    print 'OK'

# hypothetical:
from flickrAPI import FlickrAPI
flickr = FlickrAPI()
q1 = flickr.auth_oauth_checkToken()
q1 = flickr.favorites_getList(user_id=user_id)

flickr.favorites_getPublicList(user_id='whatever')

In [4]: import flickrAPI

In [5]: reload(flickrAPI)
Out[5]: <module 'flickrAPI' from 'flickrAPI.pyc'>

In [6]: flickr = flickrAPI.FlickrAPI()

In [7]: flickr.favorites_getList(user_id="test")
args ('favorites_getList',) and kwargs {'user_id': 'test'}
