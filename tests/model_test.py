import unittest
from json import loads
from reversedns import Response, ErrorMessage


_json_response_ok_empty = '''{
   "result": [],
   "size": 0
}'''

_json_response_ok = '''{
   "result": [
        {
            "value": "ac1.nstld.com 1634338343 1800 900 604800 86400",
            "name": "abc",
            "first_seen": 1634338366,
            "last_visit": 1634338366
        },
        {
            "value": "ac1.nstld.com 1634348393 1800 900 604800 86400",
            "name": "abc",
            "first_seen": 1634348416,
            "last_visit": 1634348416
        }
    ],
    "size": 2
}'''

_json_response_error = '''{
    "code": 403,
    "messages": "Access restricted. Check credits balance or enter the correct API key."
}'''


class TestModel(unittest.TestCase):

    def test_response_parsing(self):
        response = loads(_json_response_ok)
        parsed = Response(response)
        self.assertEqual(parsed.size, response['size'])
        self.assertIsInstance(parsed.result, list)
        self.assertEqual(parsed.result[0].name, response['result'][0]['name'])

    def test_error_parsing(self):
        error = loads(_json_response_error)
        parsed_error = ErrorMessage(error)
        self.assertEqual(parsed_error.code, error['code'])
        self.assertEqual(parsed_error.message, error['messages'])
