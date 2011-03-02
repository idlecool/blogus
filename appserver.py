#!/usr/bin/env python
# -*- coding: utf-8 -*-w
"""
Proxy Between HTTP server and main Application
"""

import os

# include application's caller method
# - import as run
# - arguments
#   - AppServer : AppServer object
# - return values 
#   - status  : response http status
#   - headers : response http headers
#   - output  : main output
#
from blogus import run

def apphandler(environ):
    """ Wrapper Function To Make Actual Call To The Application"""
    #DONE_CONFIGURATION = False
    #if not DONE_CONFIGURATION:
    #    status = 500
    #    headers = {
    #        "Content-Type":"text/html"
    #        }
    #    output = "<h1>AppServer Not Configured Yet</h1>"
    #    return status, headers, output
    request_headers = { 
        "REQUEST_METHOD" : environ.get("REQUEST_METHOD"),
        "PATH_INFO" : environ.get("PATH_INFO"),
        "QUERY_STRING" : environ.get("QUERY_STRING"),
        "SERVER_SOFTWARE" : environ.get("SERVER_SOFTWARE"),
        "SERVER_PROTOCOL" : environ.get("SERVER_PROTOCOL"),
        "HTTP_USER_AGENT" : environ.get("HTTP_USER_AGENT"),
        "HTTP_ACCEPT_CHARSET" : environ.get("HTTP_ACCEPT_CHARSET"),
        "HTTP_ACCEPT" : environ.get("HTTP_ACCEPT"),
        "HTTP_CONNECTION" : environ.get("HTTP_CONNECTION"),
        "HTTP_ACCEPT_LANGUAGE" : environ.get("HTTP_ACCEPT_LANGUAGE"),
        "HTTP_HOST" : environ.get("HTTP_HOST"),
        "BLOGUS_SERVER" : environ.get("BLOGUS_SERVER"),
        "CONTENT_TYPE" : environ.get("CONTENT_TYPE"),
        "CONTENT_LENGTH" : environ.get("CONTENT_LENGTH"),
        "APP_SERVER" : environ.get("APP_SERVER"),
        "SERVER_PATH" : os.path.dirname(os.path.abspath(__file__)),
        }
    status, headers, output = run(AppServer(request_headers))
    return status, headers, output

class AppServer(object):
    """
    Deployment Settings Will Go Here
    """
    def __init__(self, request_headers):
        """ All Variables Go Here """
        self.server = request_headers.pop("APP_SERVER")
        self.request_headers = request_headers
        return
