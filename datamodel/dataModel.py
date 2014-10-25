from datetime import date

class Paper(object):

    def __init__(self, title=None, authors=None, date=None, references=None,
                 api=None, api_id=None, openAccess=False):

        self.title = title
        self.authors = authors or set()
        self.date = date
        self.references = references or set()
        self.api = api
        self.api_id = api_id
        self.openAccess = openAccess




