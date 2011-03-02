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
    request = Request(environ)
    appserver = AppServer(request)
    response = run(appserver)
    status, headers, output = appserver.response.get_response()

    httpoutput = ""
    if isinstance(output, str):
        httpoutput = output
    elif isinstance(output, int):
        httpoutput = str(output)
    elif isinstance(output, dict):
        headers.update({"Content-Type": "text/plain"})
        for line in output.keys():
            httpoutput += "%s : %s\n" % (str(line), str(output[line]))
    elif isinstance(output, list):
        headers.update({"Content-Type": "text/plain"})
        httpoutput += output.join(", ")

    appserver.response.drop_write(httpoutput)

    return status, headers, httpoutput


class AppServer(object):
    """
    Defines API For interacting With HTTP Server
    """
    def __init__(self, request):
        """ All Variables Go Here """

        self.server = request.headers.pop("APP_SERVER")
        self.request = request
        self.response = Response()


class Request(object):
    """
    HTTP Request Object
    """
    def __init__(self, environ):
        self.environ = {}
        self.environ.update(environ)
        self.headers = { 
            "SCRIPT_NAME" : environ.get("SCRIPT_NAME"),
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
            "CONTENT_TYPE" : environ.get("CONTENT_TYPE"),
            "CONTENT_LENGTH" : environ.get("CONTENT_LENGTH"),
            "APP_SERVER" : environ.get("APP_SERVER"),
            "SERVER_PATH" : os.path.dirname(os.path.abspath(__file__)),
            }


class Response(object):
    """
    HTTP Response Object
    """
    def __init__(self):
        """ HTTP response varibles """

        self.headers = {"Content-Type": "text/html"
                        }
        self.status = 200
        self.output = ""

    def set_header(self, header):
        """
        Set HTTP response headers 
        """

        self.headers.update(header)

    def set_code(self, status):
        """
        Set HTTP response status code
        """

        self.status = status
        
    def write(self, output):
        """
        write output chunk by chunk
        """

        self.output = "%s%s" % (self.output, output)

    def drop_write(self, output):
        """
        drop any previous buffer and write the output
        """

        self.output = output

    def get_response(self):
        return self.status, self.headers, self.output

    def error(self, output="", status=500, header={"Content-Type":"text/html"}):
        self.output = output
        self.status = status
        self.headers.update(header)
        
