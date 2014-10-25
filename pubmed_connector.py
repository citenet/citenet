from api_connector import APIConnector

import requests
import json

from datamodel.datamodel import Paper

class PubMedConnector(APIConnector):

    def __init__(self):
        #super(PubMedConnector, self).__init__()
        self.api_id = 'pubmed'

    def create_paper(self, paper_json):
        return Paper(paper_json.setdefault('title', None), 
            paper_json.setdefault('authorString', None),
            paper_json.setdefault('pubYear', None),
            paper_json.setdefault('doi', None), 
            self.api_id, "%s,%s" % (paper_json['source'], paper_json['pmid']),
            paper_json['isOpenAccess'] == "Y", 
            paper_json['citedByCount'])

    def create_cited_paper(self, paper_json):
        url = "http://www.ebi.ac.uk/europepmc/webservices/rest/search/query=ext_id:%s src:%s&format=json" % (paper_json['id'], paper_json['source'])
        r = requests.get(url)
        result_json = json.loads(r.content)['resultList']['result'][0]
        return self.create_paper(result_json)

    def search_doi(self, doi):
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search/query=%s%%20sort_cited:y&format=json" % doi
        #print url
        r = requests.get(url)
        result_json = json.loads(r.content)['resultList']['result']
        papers = []
        references = []
        if len(result_json) > 0:
            paper_json = result_json[0]
            papers.append(self.create_paper(paper_json)) 
            #print(json.dumps(paper_json, sort_keys=True, 
            #    indent=4, separators=(',', ': ')))

            if paper_json['hasReferences'] == "Y":
                collection = paper_json['source']
                pubmed_id = paper_json['pmid']
                url = "https://www.ebi.ac.uk/europepmc/webservices/rest/%s/%s/references/1/json" % (collection, pubmed_id)

                r = requests.get(url)
                result_json = json.loads(r.content)['referenceList']['reference']

                if len(result_json) > 0:
                    #print len(result_json)
                    #reference_json = result_json[0]
                    #print(json.dumps(reference_json, sort_keys=True, 
                    #    indent=4, separators=(',', ': ')))

                    for result in result_json:
                        if result.has_key('title'):
                            #print result['title']
                            references.append(self.create_cited_paper(result))

            papers[0].references = references
        papers = papers + references

        return papers