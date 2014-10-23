#!/usr/bin/env python2.7

import sys
import flup.server.fcgi
from flup.server.fcgi import WSGIServer
from flask_bootstrap import Bootstrap
from favr3 import app

if __name__ == '__main__':
    app.debug = True
    app.secret_key = '%$#bvrfegre##Rregfdbefjklsfjklsjnm'
    Bootstrap(app)
    WSGIServer(app).run()

