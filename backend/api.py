import sys

from pubmed_connector import PubMedConnector

def search(doi, get_references=False):
    pubmed = PubMedConnector(get_date=False)
    return pubmed.search_api_id(doi, get_references)

if __name__ == '__main__':
    papers = search(sys.argv[1], True)
    print len(papers)
    for paper in papers:
        print paper.title
