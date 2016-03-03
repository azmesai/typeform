#!/usr/bin/env python

import time
import json
import urllib
import re


def lambda_handler(event, context):
    lastHourDateTime = int(time.time()) - 3600
    
    url = 'https://api.typeform.com/v0/form/FORMID?key=APIKEY&completed=true&since=%s' % lastHourDateTime
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    
    sendto = []
    for response in data['responses']:
        invite = False
        email = ""
        for key, value in response['answers'].iteritems():
            if key.encode().startswith('yesno_') and value.encode() == "1":
                invite = True
            elif key.encode().startswith('email'):
                email = value.encode()
        if invite and email:
            sendto.append( email )
    
    print sendto
    
    for newbie in sendto:
        data = urllib.urlencode({
            'email' : newbie,
            'channels':'DEFAULTCHANNELID',
            'first_name':'Newbie',
            'token':'SLACKAPITOKEN',
            'set_active':'true',
            '_attempts':'1'
        })
        print "Trying for email %s" % newbie
        f = urllib.urlopen('https://slack.com/api/users.admin.invite?t=%i' % int(time.time()) , data)
        print f.read()

