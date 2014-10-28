

class Tree(object):
    """Tree that is crawled by the crawler"""
    def __init__(self, papers=None):
        super(Tree, self).__init__()
        self.start_papers = papers[:]
        self.unwalked = papers
        self.papers = {(paper.api_name,
                        paper.api_id): paper for paper in papers}

    def paper_is_present(self, paper):

        return paper.key_tuple in self.papers

    def find_duplicate_paper(self, paper):

        return self.papers.get(paper.key_tuple, None)

    def add_new_paper(self, paper):

        self.papers[paper.key_tuple] = paper
        self.unwalked.append(paper)

    def register_citation(self, citing_paper=None, cited_paper=None):

        if cited_paper:
            duplicate = self.find_duplicate_paper(cited_paper)
            if duplicate:
                duplicate.increment_citation_count()
            else:
                self.add_new_paper(cited_paper)
            if citing_paper:
                citing_paper.append(duplicate or cited_paper)

    def remove_from_unwalked(self, paper):

        self.unwalked.remove(paper)

