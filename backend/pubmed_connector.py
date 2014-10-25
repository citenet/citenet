import json

from api_connector import APIConnector
from paper import Paper

class PubMedConnector(APIConnector):

    def __init__(self):
        self.api_name = 'pubmed'
        self.base_url = "http://www.ebi.ac.uk/europepmc/webservices/rest/"

    def create_paper(self, paper_json):
        return Paper(title=paper_json.setdefault('title', None),
            authors=paper_json.setdefault('authorString', None),
            date=paper_json.setdefault('pubYear', None),
            doi=paper_json.setdefault('doi', None),
            api_id="%s,%s" % (paper_json['source'], paper_json['pmid']),
            isOpenAccess=paper_json['isOpenAccess'] == "Y",
            global_citation_count=paper_json['citedByCount'])

    def create_cited_paper(self, paper_json):
        res = self.call("search/query=ext_id:%s src:%s&format=json" % 
            (paper_json['id'], paper_json['source']))
        result_json = json.loads(res.content)['resultList']['result'][0]
        return self.create_paper(result_json)

    def search_doi(self, doi):
        res = self.call("search/query=%s&format=json" % doi)
        return self.parse_result(res)

    def search_api_id(self, api_id):
        src, api_id = api_id.split(',')
        res = self.call("search/query=ext_id:%s src:%s&format=json" % 
            (api_id, src))
        return self.parse_result(res)

    def parse_result(self, result):
        result_json = json.loads(result.content)['resultList']['result']
        papers = []
        references = []
        if len(result_json) > 0:
            paper_json = result_json[0]
            papers.append(self.create_paper(paper_json))

            if paper_json['hasReferences'] == "Y":
                collection = paper_json['source']
                pubmed_id = paper_json['pmid']
                res = self.call("%s/%s/references/1/json" % 
                    (collection, pubmed_id))

                result_json = json.loads(res.content)['referenceList']['reference']

                if len(result_json) > 0:
                    for result in result_json:
                        if result.has_key('id') and result.has_key('title'):
                            references.append(self.create_cited_paper(result))

            papers[0].references = references
        papers = papers + references
        return papers
