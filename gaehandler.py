#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Google AppEngine Handler
"""

import os
from appserver import apphandler

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class ReqHandler(webapp.RequestHandler):
    def get(self):
        os.environ.update({
        "APP_SERVER": "GAE",
        })
        status, headers, output = apphandler(os.environ)

        if status == 301:
            self.redirect(headers["Location"], permanent=True)
        elif status == 302 or status == 307:
            self.redirect(headers["Location"])

        # status
        self.response.set_status(status)

        # headers
        for headertype in headers:
            self.response.headers.add_header(str(headertype),
                                             str(headers[headertype]))
            
        # output
        self.response.out.write(output)

application = webapp.WSGIApplication(
                                     [('/.*', ReqHandler)])

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

