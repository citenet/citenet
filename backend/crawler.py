from backend.api import search


class Crawler(object):

    def __init__(self):
        self.unwalked = []
        self.all = {}
        self.iteration_counter = 0

    def crawl(self, initial_id, max_iters):
        '''Start crawling.
               initial_id: pubmed id of the paper where the crawling
                           starts.
                max_iters: maximum number of iteration, these bascically
                           correspond to the number of API calls. not
                           to be confused with 'generations'.

        '''

        start_paper = (search(initial_id))[0]
        start_paper.depth = 0
        self.all[initial_id] = start_paper

        self.crawl_rec(initial_id, max_iters)
        self.post_filter()

        return self.all

    def crawl_rec(self, initial_id, max_iters):
        '''Recrive crawling.
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

        return search(api_id, True)

    def append_child(self, child):
        '''Updates the papers in the unwalked list and all dict. Also
           updates the local_citation_count.
               child: new paper object.

        '''

        if not child.api_id in self.all:
            if child.has_references:
                self.unwalked.append(child)
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

        if self.unwalked:
            self.unwalked.sort(key=lambda paper: paper.local_citation_count,
                               reverse=True)

            highest_citation_count = self.unwalked[0].local_citation_count

            for paper in self.unwalked:

                if paper.local_citation_count == highest_citation_count:
                    targets.append(paper)
                else:
                    break

            targets.sort(key=lambda paper: paper.depth)

        for target in targets:
            self.unwalked.remove(target)

        return targets

    def post_filter(self):

        print len(self.all.values())
        if self.all:

            all_papers = sorted(self.all.values(), key=lambda paper: paper.global_citation_count, reverse=True)

            less_globally_cited = all_papers[int(len(all_papers)*0.25):]

            for paper in less_globally_cited:

                if not paper.references and paper.local_citation_count == 1 and not paper.depth == 0:

                    self.all.pop(paper.api_id)
        print len(self.all.values())


