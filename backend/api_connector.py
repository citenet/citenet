import requests

class APIConnector(object):

    def __init__(self):
        self.api_name = ''
        self.base_url = ''

    def call(self, url, head=False):
        url = self.base_url + url
        if head:
            return requests.head(url)
        else:
            return requests.get(url)

    def call_async(self, url, session, callback):
        url = self.base_url + url
        session.get(url, background_callback=callback)

    def search_doi(self, doi, get_references=False):
        return []

    def search_api_id(self, doi, get_references=False):
        return []
