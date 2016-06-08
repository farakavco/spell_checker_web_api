import unittest
from aiohttp.web import Request
from src.scayt import *
import database

dictionary_filename = path.abspath(path.join(path.dirname(database.__file__), 'dictionary'))


class Test(unittest.TestCase):

    def test_get_lang_list(self):
        lang_request = Request()
        lang_request.GET()['cmd'] = 'get_lang_list'
        lang_result = ssrv(lang_request)
        self.assertEqual({
            "langList": {
                "ltr": {"en_US": "Persian"},
                "rtl": {}
            },
            "verLang": 6
        }, lang_result)

    def test_get_banner(self):
        banner_request = Request()
        banner_request.GET()['cmd'] = 'get_banner'
        banner_result = ssrv(banner_request)
        self.assertEqual({
            "undefined": True
        }, banner_result)

    def test_add_to_dictionary(self):
        add_request = Request()
        add_request.GET()['cmd'] = 'add_to_dictionary'
        add_request.GET()['text'] = 'test_word'
        add_result = ssrv(add_request)
        self.assertEqual({
            'Ok': True,
            'error': None
        }, add_result)
        self.assertIn('test_word', words_dictionary)
        with open(dictionary_filename, 'a', encoding='utf-8') as dictionary:
            self.assertIn('test_word', dictionary.readlines())
