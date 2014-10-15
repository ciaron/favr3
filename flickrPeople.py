from flickrBase import FlickrApiMethod

class FlickrPeopleGetInfo(FlickrApiMethod):
	"""
	Calling:
	  q=flickrPeople.FlickrPeopleGetInfi(user_id='44124394781@N01')
      q.json['stat']
	"""

	name='flickr.people.getInfo'

	def __init__(self, nojsoncallback=True, format='json', parameters=None, user_id=None):

		if user_id:
			self.user_id = user_id
		else:
			self.user_id =''

		FlickrApiMethod.__init__(self, nojsoncallback, format, parameters)
	
	def getParameters(self):
		p={
			'user_id' : self.user_id
		}
		return p
	
