import pqueue
import Pazzle

l,n,ps = Pazzle.readfromfile()
q = pqueue.PriorityQueue()
for p in ps:
    item = ((p.height, p.width), p)
    q.put(item)

for i in range(10):
    (h,w),p = q.get()
    print i
    print p.width, p.height
    print p
    print 
