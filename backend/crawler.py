from
# def walk_papers(papers):
#
#     for paper in most_connected(unwalked_papers):
#
#         for reference in paper.get_references():
#
#             childPaper = findPaperByID(reference.ID)
#
#             if not childPaper:
#                 childPaper = Paper(reference)
#                 papers[reference.ID] = childPaper
#                 unwalked_papers[reference.ID] = childPaper
#
#             childPaper.citations.add(paper)
#
#         unwalked_papers.remove(paper)

class Crawler(object):

    def __init__(self):
        self.unwalked = []
        self.all = {}


    def crawl(self, initial_doi, max_iters):
        for reference in get_references(initial_doi):


    def get_most_connected(self):
        return self.unwalked

    def get_references(self, doi):
        return [Paper(doi="1234"), Paper(doi="3456")]

    def append_child(self,child):
        if(not child in self.all):
            unwalked.append(child)



