import Pazzle

limits,n,ps = Pazzle.readfromfile()
lst = [line.strip() for line in open('submit.txt').readlines()]
nRemoved = 0
for i,n in enumerate(lst):
    if n == '':
        continue
    for ch in n:
        ps[i].operate(Pazzle.OPS[ch])
    if not ps[i].isComplete():
        print 'error: Problem No=%d' % (i+1)
        nRemoved += 1
        lst[i] = ''

ofs = open('submit.txt', 'w')
for n in lst:
    ofs.write(n)
    ofs.write('\n')
ofs.close()

print 'clean %d items.' % nRemoved
