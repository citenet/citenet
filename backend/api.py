import sys

from pubmed_connector import PubMedConnector

def search(doi, get_references=False):
    pubmed = PubMedConnector()
    return pubmed.search_api_id(doi, get_references)

if __name__ == '__main__':
    papers = search(sys.argv[1])
    for paper in papers:
        print paper.title
