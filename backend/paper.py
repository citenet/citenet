from datetime import date

class Paper(object):

    def __init__(self, title=None, authors=None, date=None, doi=None,
                 references=None, api=None, api_id=None, isOpenAccess=False, global_citation_count=0):

        self.title = title
        self.authors = authors or set()
        self.date = date
        self.doi = doi
        self.references = references or set()
        self.api = api
        self.api_id = api_id
        self.isOpenAccess = isOpenAccess
        self.local_citation_count = 1
        self.global_citation_count = global_citation_count




