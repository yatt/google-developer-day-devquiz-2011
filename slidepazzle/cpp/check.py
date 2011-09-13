import sys
import Pazzle
ifilename ='submit.txt'
if len(sys.argv) > 1:
    ifilename = sys.argv[1]

limits,n,ps = Pazzle.readfromfile()
a=0
for i,seq in enumerate(open(ifilename).readlines()):
    seq = seq.strip()
    if seq == '':
        continue
    for ch in seq:
        ps[i].operate(Pazzle.OPS[ch])
    if not ps[i].isComplete():
        print 'error: Problem No=%d %s' % (i+1, ps[i].operations())
        print ps[i]
        a += 1
print '%d errors in %s.' % (a, ifilename)
