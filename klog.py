#!/usr/bin/env python
# encoding: utf-8
"""
klog.py

Created by Keishi Hattori on 2010-07-15.
Copyright (c) 2010 Keishi Hattori. All rights reserved.
"""

import sys
import getopt
import urllib
import urllib2

import appauth

help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output=", "email=", "password="])
        except getopt.error, msg:
            raise Usage(msg)
        
        user_email = None
        user_password = None
        
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option == "--email":
                user_email = value
            if option == "--password":
                user_password = value
        
        if not user_email:
            print "ERR: You need email."
            return
        if not user_password:
            print "ERR: You need password."
            return
        
        auth = appauth.xAppAuth(user_email, user_password, 'kernlog')
        token = auth.getAuthtoken()
        resp = auth.getAuthResponse('http://kernlog.appspot.com/', 'kernlog') # this extra step sets the ASCID cookie
        try:
            r = ''
            headers = {'Authorization': 'GoogleLogin auth='+token} 
            handler = urllib2.HTTPHandler() 
            opener = urllib2.build_opener(handler)
            req = urllib2.Request('http://kernlog.appspot.com/post', urllib.urlencode({'content': 'test klog.py'}),  headers=headers)
            res = urllib2.urlopen(req)
            if res.code==200:
                r = res.read()
            return r
        except urllib2.HTTPError, e:
            return "Error Http " + str(e.code)
        except urllib2.URLError, e:
            return "Error url " + str(e.reason)
        except Exception, e:
            return "Error servidor " + str(e)
        
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
