from flickrBase import FlickrApiMethod

class FlickrAuthOAuthCheckToken(FlickrApiMethod):
	"""
	Get the authenticated/verified OAuth user, i.e. the one who allowed Favr access
	Calling:
	  q=flickrCheckToken.FlickrAuthOAuthCheckToken()

	In [3]: q.json
	Out[3]:
	{u'oauth': {u'perms': {u'_content': u'write'},
	  u'token': {u'_content': u'72157648132241640-7356d7fa77cac0e2'},
	  u'user': {u'fullname': u'Ciaron Linstead',
	   u'nsid': u'44124394781@N01',
	   u'username': u'ciaron'}},
	 u'stat': u'ok'}

	  In [7]: q.json['oauth']['user']['username']
	  Out[7]: u'ciaron'

	  In [8]: q.json['oauth']['user']['nsid']
	  Out[8]: u'44124394781@N01'
	"""

	name='flickr.auth.oauth.checkToken'

	def __init__(self, nojsoncallback=True, format='json', parameters=None, user_id=None):
		#print self.token

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
	
