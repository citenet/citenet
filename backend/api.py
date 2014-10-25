import sys

from pubmed_connector import PubMedConnector

def search(doi):
    pubmed = PubMedConnector()
    return pubmed.search_doi(doi)

if __name__ == '__main__':
    papers = search(sys.argv[1])
    for paper in papers:
        print paper.title
