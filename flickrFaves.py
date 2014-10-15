from flickrBase import FlickrApiMethod

class FlickrFavoritesGetList(FlickrApiMethod):
	"""
	Calling:
	  q=flickrFaves.FlickrFavoritesGetList(user_id='44124394781@N01')
      q.json['stat']
      q.json['photos']['total']
	"""

	name='flickr.favorites.getList'

	def __init__(self, nojsoncallback=True, format='json', parameters=None, user_id=None):

		if user_id:
			self.user_id = user_id
		else:
			self.user_id =''

		FlickrApiMethod.__init__(self, nojsoncallback, format, parameters)
	
	def getParameters(self):
		p={
			#'method'  : 'flickr.favorites.getList',
			'user_id' : self.user_id
		}
		return p
	
