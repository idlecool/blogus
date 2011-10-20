#!/usr/bin/env python
# -*- coding: utf-8 -*-w
"""
Proxy Between HTTP server and main Application
"""

import os
import re
import cgi
import urlparse
import sys
sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)), "utils"))


from blogus import run
import utils
import config

# import tenjin
# from tenjin.helpers import *
# import tenjin.gae

def apphandler(environ):
    """ Wrapper Function To Make Actual Call To The Application"""
    appserver = AppServer(environ)
    run(appserver)
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

    return status, headers, httpoutput


class AppServer(object):
    """
    Defines API For interacting With HTTP Server
    """
    def __init__(self, environ):
        """ All Variables Go Here """

        self.request = Request(environ)
        self.response = Response(self.request)
        self.context = {}
        for eachattr in dir(config):
            if not re.match("__\S+__", eachattr):
                self.context[eachattr] = getattr(config,
                                                 eachattr)


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
        self.hosturl = self.get_hosturl()
        self.pathurl = self.get_pathurl()
        self.getvars = self.get_getvars()
        self.method = self.get_method()
        self.hostprefix = self.headers.get("HTTP_HOST")
        self.hostsuffix = self.headers.get("SCRIPT_NAME")
        self.serverpath = self.get_serverpath()
        self.appserver = self.headers.get("APP_SERVER")

    def get_hosturl(self):
        """ returns url on which the blog is hosted"""

        return "http://%s%s" % (self.headers.get("HTTP_HOST"),
                         self.headers.get("SCRIPT_NAME"))

    def get_pathurl(self):
        """ returns the requested path """

        return self.headers.get("PATH_INFO")

    def get_getvars(self):
        querystring = self.headers.get("QUERY_STRING")
        qs_dict = urlparse.parse_qs(querystring)
        for eachkey in qs_dict.keys():
            listt = qs_dict[eachkey]
            qs_dict[eachkey] = []
            for eachitem in listt:
                qs_dict[eachkey].append(cgi.escape(eachitem))
        return qs_dict

    def get_method(self):
        return self.headers.get("REQUEST_METHOD")

    def get_serverpath(self):
        return os.path.dirname(os.path.abspath(__file__))

class Response(object):
    """
    HTTP Response Object
    """
    def __init__(self, request):
        """ HTTP response varibles """

        self.headers = {"Content-Type": "text/html"
                        }
        self.status = 200
        self.output = ""
        self._request = request
        self._metadata = {
            "hosturl": self._request.hosturl,
            "navbar_links": [
                ("blog","%s/blog" % self._request.hosturl),
                ("github","https://github.com/idlecool"),
                ("twitter", "http://twitter.com/idlecool"),
                ("contact", "%s/contact" % self._request.hosturl),
                ],
            }

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

    def render(self, context={}, view="base"):

        context["template_child"] = ""

        f = open(os.path.join(config.INSTALLATION_PATH,
                              "views",
                              "%s.html" % view))
        html = f.read()
        f.close()

        while html.startswith("{{ include"):
            template_parent, template_child =\
                html.split("\n", 1)
            parent_view =\
                re.findall("{{ include \S+ }}",
                           template_parent)[0][11:-3]

            context["template_child"] = template_child

            f = open(os.path.join(config.INSTALLATION_PATH,
                                  "views",
                                  "%s.html" % parent_view))
            html = f.read()
            f.close()

        varlist = re.findall("{{ \S+ }}", html)

        replacement = {}
        # remove duplicates
        for eachvar in varlist:
            replacement[eachvar] = ""

        for eachkey in replacement.keys():
            html = html.replace(eachkey,
                                context[eachkey[3:-3]])

        self.drop_write(html)
