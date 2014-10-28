import requests
from redis_cache import cache_it

@cache_it(limit=1000, expire=60 * 60 * 24 * 30)
def make_call(url, head):
    print "make_call", url
    if head:
        return requests.head(url)
    else:
        return requests.get(url) 

class APIConnector(object):

    def __init__(self):
        self.api_name = ''
        self.base_url = ''

    def call(self, url, head=False):
        url = self.base_url + url
        print "call", url
        return make_call(url, head)

    def call_async(self, url, session, callback):
        url = self.base_url + url
        print "call_async", url
        session.get(url, background_callback=callback)

    def search_doi(self, doi, get_references=False):
        return []

    def search_api_id(self, doi, get_references=False):
        return []
