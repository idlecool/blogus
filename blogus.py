#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from utils import *
import config

def run(appserver):
    """
    Wrapper to finally make call to the Application
    """

    urlhandler = UrlHandler(appserver)

class UrlHandler(object):
    """ url mapping service """

    def __init__(self, appserver):
        """ store request headers """

        # request method
        self.method = appserver.request.headers.get("REQUEST_METHOD")
        # request url
        self.path = appserver.request.headers.get("PATH_INFO")
        # installation dir offset
        self.scriptname = appserver.request.headers.get("SCRIPT_NAME")
        if self.scriptname!="" and self.scriptname != "/":
            if self.scriptname[-1] != "/":
                self.scriptname = "%s/" % self.scriptname
        else:
            if self.scriptname == "/":
                self.scriptname = ""
        # host
        self.httphost = appserver.request.headers.get("HTTP_HOST")
        # preparing GET vars
        from cgi import parse_qs, escape
        self.getvars = parse_qs(appserver.request.headers.get("QUERY_STRING"))
        # sanitize GET vars
        for getvar in self.getvars.keys():
            for each in self.getvars[getvar]:
                self.getvars[getvar].append(escape(each))
        # blogus url
        self.blogusurl = "%s/%s" % (self.httphost, self.scriptname)

        # all root level static files goes here
        if self.path in ("/favicon.ico", "/robots.txt"):
            appserver.response.set_header({
                    "Location":"/static%s" % self.path,
                    })
            appserver.response.set_code(301)
        else:
            appserver.response.drop_write(self.path)
