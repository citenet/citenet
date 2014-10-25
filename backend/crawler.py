from backend.api import search

class Crawler(object):

    def __init__(self):
        self.unwalked = []
        self.all = {}
        self.iteration_counter = 0

    def crawl(self, initial_id, max_iters):
        self.all[initial_id] = (search(initial_id))[0]
        self.crawl_rec(initial_id, max_iters)
        return self.all

    def crawl_rec(self, initial_id, max_iters):
        for reference in self.get_references(initial_id):
            self.append_child(reference)
            print initial_id, reference.api_id
            self.all[initial_id].references.append(reference.api_id)

        for target in self.pick_next_targets():
            if self.iteration_counter < max_iters:
                self.iteration_counter += 1
                self.crawl_rec(target.api_id, max_iters)


    def get_references(self, api_id):
        return search(api_id, True)

    def append_child(self, child):
        if not child.api_id in self.all:
            self.unwalked.append(child)
            self.all[child.api_id] = child
        else:
            self.all[child.api_id].local_citation_count += 1

    def pick_next_targets(self):
        if self.unwalked:
            self.unwalked.sort(key=lambda paper: paper.local_citation_count, reverse=True)
            if len(self.unwalked) > 3:
                targets = self.unwalked[:3]
            else:
                targets = self.unwalked
            for target in targets:
                self.unwalked.remove(target)
            return targets
        else:
            return []


