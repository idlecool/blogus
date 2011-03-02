#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *

def run(appserver):
    """
    Wrapper to finally make call to the Application
    """
    status = ""
    headers = {}
    output = ""

    status = 200
    headers = {
        "Content-Type": "text/plain",
        }
    output = "YuHoo"

    return status, headers, output
