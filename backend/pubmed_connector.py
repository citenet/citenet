import json, requests, datetime, math
from requests_futures.sessions import FuturesSession

from api_connector import APIConnector
from paper import Paper

class PubMedConnector(APIConnector):

    def __init__(self, get_date=True):
        self.api_name = 'pubmed'
        self.base_url = "http://www.ebi.ac.uk/europepmc/webservices/rest/"
        self.get_date = get_date
        self.references = []

    def create_paper(self, paper_json):
        if paper_json.has_key('pmid'):
            date = None
            if self.get_date and paper_json.has_key('doi'):
                res = requests.get("http://api.crossref.org/works/%s" % paper_json['doi'])
                if res.status_code == 200:
                    date = json.loads(res.content)['message']['issued']['date-parts'][0]
                    while len(date) < 3:
                        date.append(1)
                    year, month, day = date
                    date = str(datetime.date(year, month, day))
            if date == None:
                if paper_json.has_key('pubYear'):
                    date = str(datetime.date(int(paper_json['pubYear']), 1, 1))
                else:
                    date = None

            return Paper(
                api=self.api_name,
                title=paper_json.setdefault('title', None),
                authors=paper_json.setdefault('authorString', None),
                date=date,
                doi=paper_json.setdefault('doi', None),
                api_id="%s,%s" % (paper_json['source'], paper_json['pmid']),
                isOpenAccess=paper_json['isOpenAccess'] == "Y",
                global_citation_count=paper_json['citedByCount'],
                has_references=(paper_json['hasReferences'] == "Y"))

    def create_cited_paper(self, paper_json):
        res = self.call("search/query=ext_id:%s src:%s&format=json" % 
            (paper_json['id'], paper_json['source']))
        result_json = json.loads(res.content)['resultList']['result'][0]
        return self.create_paper(result_json)

    def search_doi(self, doi, get_references=False):
        res = self.call("search/query=%s&format=json" % doi)
        return self.parse_result(res, get_references)

    def search_api_id(self, api_id, get_references=False):
        src, api_id = api_id.split(',')
        res = self.call("search/query=ext_id:%s src:%s&format=json" % 
            (api_id, src))
        return self.parse_result(res, get_references)

    def process_references_page(self, res):
        result_json = res.json()['referenceList']['reference']

        if len(result_json) > 0:
            for result in result_json:
                if result.has_key('id') and result.has_key('title'):
                    reference = self.create_cited_paper(result)
                    if reference:
                        self.references.append(reference)

    def parse_result(self, result, get_references=False):
        result_json = json.loads(result.content)['resultList']['result']
        papers = []
        self.references = []
        if len(result_json) > 0:
            paper_json = result_json[0]
            if not get_references:
                papers.append(self.create_paper(paper_json))

            if get_references and paper_json['hasReferences'] == "Y":
                collection = paper_json['source']
                pubmed_id = paper_json['pmid']

                res = self.call("%s/%s/references/%i/json" % 
                        (collection, pubmed_id, 1))

                result_json = res.json()
                hits = result_json['hitCount']
                result_json = result_json['referenceList']['reference']
                self.process_references_page(res)

                session = FuturesSession(max_workers=5)
                for i in range(2, int(math.ceil(hits / 25.0) + 1)):
                    self.call_async("%s/%s/references/%i/json" % 
                        (collection, pubmed_id, i), session, 
                        self.process_references_page)

            if not get_references:
                papers[0].references = self.references
        papers = papers + self.references
        return papers
