#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Apache HTTP Server `mod_wsgi` handler

needs apache2x, mod_wsgi, python-virtualenv(optional)

Generate Python Virtual Environment (virtualenv)

# cd /usr/share
# mkdir python-wsgi
# cd $_
# virtualenv --no-site-packages wsgi-baseline-python

Example Configuaration which has to be added into apache config file
(httpd.conf):

LoadModule wsgi_module modules/mod_wsgi.so
AddHandler wsgi-script .wsgi
WSGIPythonHome /usr/share/python-wsgi/wsgi-baseline-python

http://code.google.com/p/modwsgi/wiki/QuickConfigurationGuide
"""

import os, sys
import BaseHTTPServer

#current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# set script directory as current directory
os.chdir(current_directory)

# put this script directory into import path
try:
    sys.path.remove(current_directory)
except(ValueError):
    pass
sys.path.insert(0, current_directory)


from appserver import apphandler

statuscodes=BaseHTTPServer.BaseHTTPRequestHandler.responses

def application(environ, start_response):
    response_headers = []
    
    # custom environment variables
    environ.update({
            "APP_SERVER": "MOD_WSGI",
            })

    status, headers, output = apphandler(environ)

    for headertype in headers.keys():
        response_headers.append((
                str(headertype),
                str(headers[headertype]),
                ))
    status = "%s %s" % (str(status),
                        statuscodes[status][0])
    start_response(status, response_headers)
    return [output]
