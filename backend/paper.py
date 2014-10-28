

class Paper(object):
    '''Paper object. Stores all kind of properties corresponding to
       one paper.

    '''

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
        self.crawled_in_iteration = 0

    def as_dict(self):
        '''Returns relavant attributes in a dict. Can be used later on
           to create JSON.

        '''
        dictionary = {"title": self.title,
                      "authors": self.authors,
                      "date": self.date,
                      "doi": self.doi,
                      "references": [reference.api_id for reference in self.references],
                      "api": self.api,
                      "api_id": self.api_id,
                      "isOpenAccess": self.isOpenAccess,
                      "local_citation_count": self.local_citation_count,
                      "global_citation_count": self.global_citation_count,
                      "crawled_in_iteration": self.crawled_in_iteration
                      }

        return dictionary

    def increment_citation_count(self):
        self.local_citation_count += 1

    @property
    def key_tuple(self):
        return (self.api, self.api_id)





