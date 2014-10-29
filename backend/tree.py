

class Tree(object):
    """Tree that is crawled by the crawler"""
    def __init__(self, papers=None):
        super(Tree, self).__init__()
        if papers:
            self.start_papers = papers[:]
            self.unwalked = papers
            self.papers = {(paper.api_name,
                            paper.api_id): paper for paper in papers}
        else:
            self.start_papers = []
            self.unwalked = []
            self.papers = {}

    def paper_is_present(self, paper):
        '''Bool: True if paper is in the tree.'''

        return paper.key_tuple in self.papers

    def find_duplicate_paper(self, paper):

        return self.papers.get(paper.key_tuple, None)

    def add_new_paper(self, paper):

        self.papers[paper.key_tuple] = paper
        if paper.has_references:
            self.unwalked.append(paper)

    def register_citation(self, citing_paper=None, cited_paper=None):

        if cited_paper:
            duplicate = self.find_duplicate_paper(cited_paper)
            if duplicate:
                duplicate.increment_citation_count()
            else:
                self.add_new_paper(cited_paper)
            if citing_paper:
                citing_paper.references.append(duplicate or cited_paper)

    def remove_from_unwalked(self, paper):

        if paper in self.unwalked:

            self.unwalked.remove(paper)

    def as_dict(self):

        return {key_tuple[1]: paper.as_dict() for key_tuple, paper in self.papers.items()}

    def as_list(self):

        return [paper.as_dict() for paper in self.papers.values()]


