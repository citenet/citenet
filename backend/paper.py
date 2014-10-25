from datetime import date

class Paper(object):

    def __init__(self, title=None, authors=None, date=None, doi=None,
                 references=None, api=None, api_id=None, isOpenAccess=False,
                 global_citation_count=0, has_references=False):

        self.title = title
        self.authors = authors or []
        self.date = date
        self.doi = doi
        self.references = references or []
        self.api = api
        self.api_id = api_id
        self.isOpenAccess = isOpenAccess
        self.local_citation_count = 1
        self.global_citation_count = global_citation_count
        self.has_references = has_references
        self.walked = False
        self.depth = None


    def as_dict(self):
        dictionary = {
        "title": self.title,
        "authors": self.authors,
        "date": self.date,
        "doi": self.doi,
        "references": self.references,
        "api": self.api,
        "api_id": self.api_id,
        "isOpenAccess": self.isOpenAccess,
        "local_citation_count": self.local_citation_count,
        "global_citation_count": self.global_citation_count,
        }
        return dictionary




