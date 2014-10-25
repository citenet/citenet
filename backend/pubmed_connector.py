import json

from api_connector import APIConnector
from datamodel import Paper

class PubMedConnector(APIConnector):

    def __init__(self):
        self.api_id = 'pubmed'
        self.base_url = "http://www.ebi.ac.uk/europepmc/webservices/rest/"

    def create_paper(self, paper_json):
        return Paper(paper_json.setdefault('title', None), 
            paper_json.setdefault('authorString', None),
            paper_json.setdefault('pubYear', None),
            paper_json.setdefault('doi', None), 
            self.api_id, "%s,%s" % (paper_json['source'], paper_json['pmid']),
            paper_json['isOpenAccess'] == "Y", 
            paper_json['citedByCount'])

    def create_cited_paper(self, paper_json):
        r = self.call("search/query=ext_id:%s src:%s&format=json" % (paper_json['id'], paper_json['source']))
        result_json = json.loads(r.content)['resultList']['result'][0]
        return self.create_paper(result_json)

    def search_doi(self, doi):
        r = self.call("search/query=%s%%20sort_cited:y&format=json" % doi)
        result_json = json.loads(r.content)['resultList']['result']
        papers = []
        references = []
        if len(result_json) > 0:
            paper_json = result_json[0]
            papers.append(self.create_paper(paper_json))

            if paper_json['hasReferences'] == "Y":
                collection = paper_json['source']
                pubmed_id = paper_json['pmid']
                r = self.call("%s/%s/references/1/json" % (collection, pubmed_id))

                result_json = json.loads(r.content)['referenceList']['reference']

                if len(result_json) > 0:

                    for result in result_json:
                        if result.has_key('title'):
                            references.append(self.create_cited_paper(result))

            papers[0].references = references
        papers = papers + references

        return papers