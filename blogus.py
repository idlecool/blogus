#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


import utils
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

        # all root level static files goes here
        if appserver.request.pathurl in ("/favicon.ico", "/robots.txt"):
            appserver.response.set_header({
                    "Location":"%s%s" % (appserver.context["site_cdn_path"],
                                                appserver.request.pathurl),
                    })
            appserver.response.set_code(301)
        else:
            if appserver.request.pathurl == "/":
                context = appserver.context
                context.update({"page_content": "nothing",
                                "page_title": "Home"})
                appserver.response.render(context=context, view="home")
            else:
                context = appserver.context
                context.update({"page_content": "nothing",
                                "page_title": "There is nothing like Python"})
                appserver.response.render(context=context, view="post")

