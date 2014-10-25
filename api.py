import sys
import requests
import json

def main():
    doi = sys.argv[1]
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search/query=%s%%20sort_cited:y&format=json" % doi
    print url
    r = requests.get(url)
    result_json = json.loads(r.content)['resultList']['result']
    if len(result_json) > 0:
        paper_json = result_json[0]
        print(json.dumps(paper_json, sort_keys=True, 
            indent=4, separators=(',', ': ')))

        if paper_json['hasReferences'] == "Y":
            collection = paper_json['source']
            pubmed_id = paper_json['pmid']
            url = "https://www.ebi.ac.uk/europepmc/webservices/rest/%s/%s/references/1/json" % (collection, pubmed_id)

            r = requests.get(url)
            result_json = json.loads(r.content)['referenceList']['reference']

            if len(result_json) > 0:
                print len(result_json)
                reference_json = result_json[0]
                print(json.dumps(reference_json, sort_keys=True, 
                    indent=4, separators=(',', ': ')))

if __name__ == '__main__':
    main()
