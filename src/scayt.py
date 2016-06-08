import asyncio
import json
from os import path
import re
from faspell.spell_checker import SpellChecker
from aiohttp import web
import database
dictionary_filename = path.abspath(path.join(path.dirname(database.__file__), 'dictionary'))


class Dictionary(object):
    def __init__(self, filename):
        self.database = filename
        self.load()

    def add_word(self, word):
        words_dictionary[word] = 1
        self.dump(word)

    def dump(self, word):
        with open(self.database, 'a', encoding='utf-8') as dictionary:
            dictionary.write('%s%s' % ('\n', word))

    def make_words(self, database):
        return re.split('\n', database)

    def train(self, words):
        return dict.fromkeys(words, 1)

    def load(self):
        with open(self.database, 'r', encoding='utf-8') as my_file:
            return self.train(self.make_words(my_file.read()))


words_dictionary = Dictionary(dictionary_filename).load()


def get_lang_list():

    return {
        "langList": {
            "ltr": {"en_US": "Persian"},
            "rtl": {}
        },
        "verLang": 6
    }


def get_banner():
    return {
        "undefined": True
    }


def add_to_dictionary(text):
    my_dictionary = Dictionary(dictionary_filename)
    my_dictionary.add_word(text)
    return {
        'Ok': True,
        'error': None
    }


def check_spelling(text):
    check = SpellChecker(words_dictionary)
    return check.correct(text)

async def ssrv(request):
    if request.GET['cmd'] == 'get_lang_list':
        result = get_lang_list()
    elif request.GET['cmd'] == 'getbanner':
        result = get_banner()
    elif request.GET['cmd'] == 'check_spelling':
        result = check_spelling(request.GET['text'])
    elif request.GET['cmd'] == 'add_to_dictionary':
        return add_to_dictionary(request.GET['text'])
    else:
        raise NotImplementedError
    # print('%s(%s)' % (request.GET['callback'], json.dumps(result)))
    return web.Response(body=('%s(%s)' % (request.GET['callback'], json.dumps(result))).encode())

app = web.Application()
app.router.add_route('GET', '/scayt/ssrv.json', ssrv)


if __name__ == '__main__':
    web.run_app(app)
