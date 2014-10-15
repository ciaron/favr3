from flickrBase import FlickrApiMethod

class FlickrTestLogin(FlickrApiMethod):

	name = 'flickr.test.login'

	def __init__(self, nojsoncallback=True, format='json', parameters=None):
		FlickrApiMethod.__init__(self, nojsoncallback, format, parameters)
	
	def getParameters(self):
		p={
			#'method'  : 'flickr.favorites.getList',
		}
		return p
	
	
