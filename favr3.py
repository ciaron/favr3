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
