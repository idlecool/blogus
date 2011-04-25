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
                    "Location":"%s/static%s" % (appserver.request.hostsuffix,
                                                appserver.request.pathurl),
                    })
            appserver.response.set_code(301)
        else:
            context = {
                'title': 'Tenjin Example',
                'items': ['<AAA>', 'B&B', '"CCC"'],
                }
            appserver.response.render(template_name="home.pyhtml",
                                      template_data=context)
