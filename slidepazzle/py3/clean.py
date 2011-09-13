import Pazzle

limits,n,ps = Pazzle.readfromfile()
lst = eval(open('cal.txt').read())
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

ofs = open('cal.txt', 'w')
ofs.write(repr(lst))
ofs.close()

print 'clean %d items.' % nRemoved
