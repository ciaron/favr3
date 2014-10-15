class APIKeys(object):
    """Base class to read the APIKeys from file"""

    def __init__(self,filename='apikeys'):
        try:
            fp = open(filename)
        except IOError as e:
            raise
        else:
            with fp:
                self.apikey = fp.readline().rstrip('\n')
                self.apisecret = fp.readline().rstrip('\n')
                fp.close()

class TokenKeys(object):
    """Base class to read the Access Tokens"""

    def __init__(self,filename='token'):
        try:
            fp = open(filename)
        except IOError as e:
            raise
        else:
            with fp:
                self.token = fp.readline().rstrip('\n')
                self.secret = fp.readline().rstrip('\n')
                fp.close()
