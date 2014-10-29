

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
        '''Returns the paper object that describes the same physical
           paper as the paper used as an input, if this paper object
           was already part of the tree.
        '''

        return self.papers.get(paper.key_tuple, None)

    def add_new_paper(self, paper):
        '''Add a new paper to the tree. If the paper has its
           has_references attribute set to True, it will automatically
           be added to the list of unwalked nodes.
        '''

        self.papers[paper.key_tuple] = paper
        if paper.has_references:
            self.unwalked.append(paper)

    def register_citation(self, citing_paper=None, cited_paper=None):
        '''Register a citation from one paper to another. If the cited
           paper is not in the tree yet it will be added.
        '''

        if cited_paper:
            duplicate = self.find_duplicate_paper(cited_paper)
            if duplicate:
                duplicate.increment_citation_count()
            else:
                self.add_new_paper(cited_paper)
            if citing_paper:
                citing_paper.references.append(duplicate or cited_paper)

    def remove_from_unwalked(self, paper):
        '''Remove paper from unwalked nodes.'''

        if paper in self.unwalked:

            self.unwalked.remove(paper)

    def as_dict(self):
        '''Returns a dict describing the papers in the tree.'''

        return {paper.api_id: paper.as_dict() for paper in self.papers.values()}

    def as_list(self):
        '''Returns a list of papers in the tree.'''

        return [paper.as_dict() for paper in self.papers.values()]


