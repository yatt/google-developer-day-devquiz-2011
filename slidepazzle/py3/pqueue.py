from Queue import Queue
from heapq import heappush, heappop

class PriorityQueue(Queue):
    def _init(self, maxsize=0):
        self.maxsize = maxsize
        self.queue = []
    def _put(self, item):
        return heappush(self.queue, item)
    def _get(self):
        return heappop(self.queue)
    def empty(self):
        return len(self.queue) == 0
