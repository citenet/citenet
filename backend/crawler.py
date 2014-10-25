from backend.api import search

class Crawler(object):

    def __init__(self):
        self.unwalked = []
        self.all = {}
        self.iteration_counter = 0

    def crawl(self, initial_id, max_iters):
        self.crawl_rec(initial_id, max_iters)
        for paper in self.all.values():
            for i, reference in enumerate(paper.references):
                paper.references[i] = reference.api_id
        return self.all

    def crawl_rec(self, initial_id, max_iters):
        for reference in self.get_references(initial_id):
            self.append_child(reference)

        for target in self.pick_next_targets():
            if self.iteration_counter < max_iters:
                self.iteration_counter += 1
                self.crawl_rec(target , max_iters)

    def get_most_connected(self):
        return self.unwalked

    def get_references(self, api_id):
        return search(api_id)

    def append_child(self, child):
        if(not child.api_id in self.all):
            self.unwalked.append(child)
            self.all[child.api_id] = child
        else:
            self.all[child.api_id].local_citation_count += 1


    def pick_next_targets(self):
        self.unwalked.sort(key=lambda paper: paper.local_citation_count, reverse=True)
        return [self.unwalked[0]]

