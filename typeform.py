import time
import json
from urllib import request, parse
import os

# Slack Params
DEFAULT_CHANNEL_ID = os.environ['DEFAULT_CHANNEL_ID']
SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']

# Typeform Params
FORM_ID = os.environ['FORM_ID']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
FULL_NAME_FIELD = os.environ['FULL_NAME_FIELD']
AGREE_FIELD = os.environ['AGREE_FIELD']
EMAIL_FIELD = os.environ['EMAIL_FIELD']


def send_invite(email, full_name):
    params = parse.urlencode({
        'email': email,
        'channels': DEFAULT_CHANNEL_ID,
        'first_name': full_name,
        'token': SLACK_API_TOKEN,
        'set_active': 'true',
        '_attempts': '1'

    }).encode("utf-8")

    print("Trying for email %s" % email)

    req = request.Request('https://slack.com/api/users.admin.invite?')
    with request.urlopen(req, params) as response:
        data = json.loads(response.read())
        print(data)


def lambda_handler(event, context):
    last_hour_date_time = int(time.time()) - 3600
    url = ('https://api.typeform.com/forms/%s/responses?completed=true&since=%s' % (FORM_ID, last_hour_date_time))
    headers = {'Content-Type': "application/json", "Authorization": "Bearer " + ACCESS_TOKEN}
    req = request.Request(url=url, headers=headers)

    with request.urlopen(req) as response:
        data = json.loads(response.read())

    for response in data['items']:
        _data = {}
        for i in response["answers"]:
            if i["field"]["id"] in [FULL_NAME_FIELD, AGREE_FIELD, EMAIL_FIELD]:
                _data[i["field"]["id"]] = i[i["type"]]

        if _data[AGREE_FIELD] and _data[EMAIL_FIELD]:
            send_invite(_data[EMAIL_FIELD], _data[FULL_NAME_FIELD])
