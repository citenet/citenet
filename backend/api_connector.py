import requests

class APIConnector(object):

    def __init__(self):
        self.api_name = ''
        self.base_url = ''

    def call(self, url):
        url = self.base_url + url
        return requests.get(url)

    def search_doi(self, doi, get_references=False):
        return []

    def search_api_id(self, doi, get_references=False):
        return []
