from backend.api import get_references_for_paper, search
from backend.tree import Tree


class Crawler(object):
    '''Crawler class. most important method is crawl.

    '''

    def __init__(self):
        '''Init'''

        self.tree = Tree()
        self.iteration_counter = 0

    def crawl(self, initial_id, max_iters):
        '''Start crawling.
               args:
               initial_id: pubmed id of the paper where the crawling
                           starts.
                max_iters: maximum number of iteration, these bascically
                           correspond to the number of API calls. not
                           to be confused with 'generations'.

        '''
        print 'a'
        start_paper = (search('pubmed', initial_id))[0]
        self.tree.add_new_paper(start_paper)
        start_paper.depth = 0
        references = get_references_for_paper(start_paper)
        print references
        for reference in references:
            print 'ttt'
            self.tree.register_citation(citing_paper=start_paper,
                                        cited_paper=reference)
            reference.depth = start_paper.depth + 1

        self.tree.remove_from_unwalked(start_paper)
        self.crawl_linear(max_iters)
        self.post_filter()
        print 'b'
        return self.tree.papers

    def crawl_linear(self, max_iters):
        print 'aaaaa'
        while self.tree.unwalked:

            for paper in self.pick_next_targets():

                if self.iteration_counter > max_iters:
                    return
                self.iteration_counter += 1
                print self.iteration_counter

                for reference in get_references_for_paper(paper):
                    reference.depth = paper.depth + 1
                    self.tree.register_citation(citing_paper=paper,
                                                cited_paper=reference)
                self.tree.remove_from_unwalked(paper)

    def crawl_linear_old(self, initial_id, max_iters):
        '''Non-recursive crawler. Takes the papers with the highest
           citation scores in the local network and finds the references
           for them. The order of crawling is different than in the
           recursive version. More (filtered) breadth first.
                args:
                initial_id: pubmed id of the paper where the crawling
                           starts.
                max_iters: maximum number of iteration, these bascically
                           correspond to the number of API calls. not
                           to be confused with 'generations'.

        '''

        # Setting up the first paper in the model as a starting point.
        start_paper = self.all[initial_id]
        references_of_first_paper = self.get_references(initial_id)
        for paper in references_of_first_paper:
            start_paper.references.append(paper.api_id)
            paper.depth = 1
            self.append_child(paper)

        # Walk

        while True:

            if not self.unwalked:
                return

            for paper in self.pick_next_targets():

                if self.iteration_counter > max_iters:
                    return
                self.iteration_counter += 1
                print self.iteration_counter

                for reference in self.get_references(paper.api_id):
                    reference.depth = paper.depth + 1
                    self.append_child(reference)
                    paper.references.append(reference.api_id)

    def crawl_rec(self, initial_id, max_iters):
        '''Recursive crawling.
                args:
                initial_id: pubmed id of the paper where the crawling
                           starts.
                max_iters: maximum number of iteration, these bascically
                           correspond to the number of API calls. not
                           to be confused with 'generations'.

        '''

        initial_paper = self.all[initial_id]
        child_depth = initial_paper.depth + 1

        for reference in self.get_references(initial_id):
            reference.depth = child_depth
            self.append_child(reference)
            initial_paper.references.append(reference.api_id)

        for target in self.pick_next_targets():
            if self.iteration_counter < max_iters:
                self.iteration_counter += 1
                target.walked = True
                self.crawl_rec(target.api_id, max_iters)

    def get_references(self, api_id):
        '''Get all references for an id, for now the pubmed id.
        '''
        pass
        #return search(api_id, True)

    def append_child(self, child):
        '''Updates the papers in the unwalked list and all dict. Also
           updates the local_citation_count.
               args: child: new paper object.

        '''

        if not child.api_id in self.all:
            if child.has_references:
                self.unwalked.append(child)
            child.crawled_in_iteration = self.iteration_counter
            self.all[child.api_id] = child
        else:
            self.all[child.api_id].local_citation_count += 1

    def pick_next_targets(self):
        '''Defines how the papers to be crawled next are selected from
           the uncrawled paper list. All papers that have the highest
           citation count in the local network are returned. There can
           be can be several papers have the same citation count.

        '''

        targets = []

        if self.tree.unwalked:
            self.tree.unwalked.sort(key=lambda paper: paper.local_citation_count,
                                    reverse=True)
            highest_citation_count = self.tree.unwalked[0].local_citation_count

            for paper in self.tree.unwalked:
                if paper.local_citation_count == highest_citation_count:
                    targets.append(paper)
                else:
                    break

            targets.sort(key=lambda paper: paper.depth)

        return targets

    def post_filter(self, cutoff=0.25):
        '''Is called after the actual crawling process is done. Removes
           some nodes that possibly visually cluther the network. For
           these nodes there is no reference information and they are
           also not cited by more than one other paper. Also they don't
           belong to the most globally cited papers in this
           list.
               args: cutoff: the fraction of papers that should be
                             kept in the network. These are the papers
                             with the highest global citation count.
                             default: 0.25

        '''

        if self.tree.papers:

            all_papers = self.tree.papers.values()

            if len(all_papers) > 300:

                all_papers.sort(key=lambda paper: (paper.local_citation_count,
                                paper.global_citation_count), reverse=True)

                for paper in all_papers[300:]:
                    self.tree.papers.pop(paper.key_tuple)
                print len(self.all.values())

            elif len(all_papers) > 100:

                less_connected_papers = [paper for paper in all_papers if not paper.references and paper.local_citation_count==1 and not paper.depth <= 1]

                less_connected_papers.sort(key=lambda paper: (paper.global_citation_count))

                for paper in less_connected_papers[int(len(less_connected_papers)*cutoff):]:
                                                   self.tree.papers.pop(paper.key_tuple)




