import sys

from pubmed_connector import PubMedConnector

connector_by_api_name = {'pubmed': PubMedConnector}


def search(api_name, api_id, get_references=False, get_date=False):

    connectorType = connector_by_api_name[api_name]
    connector = connectorType(get_date=get_date)

    return connector.search_api_id(api_id, get_references)

def get_references_for_paper(paper):

    '''Get the reference list for a paper.

    '''

    return search(paper.api, paper.api_id, True)



if __name__ == '__main__':
    papers = search(sys.argv[1], True)
    print len(papers)
    for paper in papers:
        print paper.title




