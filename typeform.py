#!/usr/bin/env python

import time
import json
import urllib
import re
from contextlib import closing

FORMID = "FORMID"
APIKEY = "APIKEY"
DEFAULTCHANNELID = "DEFAULTCHANNELID"
SLACKAPITOKEN = "SLACKAPITOKEN"

FULL_NAME_FIELD = "textfield_10651691"
AGREE_FIELD = "yesno_10651767"
EMAIL_FIELD = "email_10651738"


def send_invite(email, full_name):
    data = urllib.urlencode({
        'email': email,
        'channels': DEFAULTCHANNELID,
        'first_name': full_name,
        'token': SLACKAPITOKEN,
        'set_active': 'true',
        '_attempts': '1'
    })
    print "Trying for email %s" % email
    with closing(urllib.urlopen(
            'https://slack.com/api/users.admin.invite?t=%i' % int(
                time.time()), data)) as f:
        print f.read()


def lambda_handler(event, context):
    lastHourDateTime = int(time.time()) - 3600

    url = ('https://api.typeform.com/v0/form/'
           '%s?key=%s&completed=true&since=%s' % (
               FORMID, APIKEY, lastHourDateTime))
    with closing(urllib.urlopen(url)) as response:
        data = json.loads(response.read())

    for response in data['responses']:
        answers = response['answers']
        email = answers[EMAIL_FIELD].encode()
        invite = (answers[AGREE_FIELD] == "1")
        full_name = answers[FULL_NAME_FIELD]
        if invite and email:
            send_invite(email, full_name)
