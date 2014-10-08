import config # local config, API Key, Secret etc.
import flickrapi

# get public favorites
faves = flickr.favorites_getPublicList(user_id=config.USER)

# get all favorites
# (requires authenticated access)
faves = flickr.favorites_getList(user_id=config.USER)
