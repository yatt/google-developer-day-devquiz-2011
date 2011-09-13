class BreadthFirstSearchTarget(object):
    def isComplete(self):
        pass
    def process(self, branch):
        pass
    def branches(self):
        pass

class AnswerIsNotFound(Exception):
    pass

class BreadthFirstSearch(object):
    def __init__(self, maxdepth):
        self.maxdepth = maxdepth
    
    def _search(self, target):
        self.q.put((0, target))
        while not self.q.empty():
            depth, target = self.q.get()
            for branch in target.branches():
                target.process(branch)
                if target.isComplete():
                    return target
                if depth < self.maxdepth and not self.isCut(depth, target):
                    self.q.put((depth + 1, copy.deepcopy(target)))
        raise AnswerIsNotFound()
    
    def isCut(self):
        return False
    
    def search(self, target):
        self.q = Queue.Queue()
        self._search(target)
        self.q = None

