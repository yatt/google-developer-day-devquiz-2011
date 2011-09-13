import sys
import random
import Pazzle

pid  = int(sys.argv[1])
nmax = int(sys.argv[2])

l,n,ps = Pazzle.readfromfile()
p = ps[pid - 1]
visited = set()
while True:
    p.reset()
    for i in range(nmax):
        ops = p.operatables()
        op = random.choice(ops)
        p.operate(op)
        if p.isComplete():
            print p.operations()
            sys.exit()
print None
