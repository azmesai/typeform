import unittest
import json
from mock import patch, call

from typeform import lambda_handler


def gimmeanswer(yesno, email, full_name):
    return {'answers': {
        'yesno_10651767': yesno,
        'email_10651738': email,
        'textfield_10651691': full_name,
        }
    }
 
test_input = {
    'responses': [
        gimmeanswer('1', 'gmail@chucknorris.com', 'Chuck Norris'),
        gimmeanswer('0', 'abc@def.com', 'abc def'),
        gimmeanswer('1', '', 'some name')
    ]
}


class TestCase(unittest.TestCase):
    @patch('urllib.urlopen')
    @patch('time.time')
    def test_typeform(self, time, urlopen):
        time.return_value = 3610
        urlopen.return_value.read.return_value = json.dumps(test_input)
        lambda_handler(None, None)
        self.assertEquals(len(urlopen.mock_calls), 6)
        self.assertEquals(urlopen.mock_calls[0], call('https://api.typeform.com/v0/form/FORMID?key=APIKEY&completed=true&since=10'))
        self.assertEquals(urlopen.mock_calls[1], call().read())
        self.assertEquals(urlopen.mock_calls[2], call().close())
        self.assertEquals(urlopen.mock_calls[3], call('https://slack.com/api/users.admin.invite?t=3610', 'first_name=Chuck+Norris&set_active=true&_attempts=1&channels=DEFAULTCHANNELID&token=SLACKAPITOKEN&email=gmail%40chucknorris.com'))
        self.assertEquals(urlopen.mock_calls[4], call().read())
        self.assertEquals(urlopen.mock_calls[5], call().close())

