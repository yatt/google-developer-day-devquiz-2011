import sys
if len(sys.argv) < 3:
    print 'usage: %s file1 file2' % __file__
    sys.exit()

f1 = sys.argv[1]
f2 = sys.argv[2]

lst = [line.strip() for line in open(f1).readlines()]
mst = [line.strip() for line in open(f2).readlines()]
nst = ['']*len(lst)
for i,(l,m) in enumerate(zip(lst, mst)):
    item = ''
    if l != '':
        item = l
    if (m != '' and l == '') or (m != '' and l != '' and len(m) < len(l)):
        item = m
    if (l != '' or m != '') and l != m:
        sys.stderr.write('%d merged %s %s\n' % (i+1, l, m))
    nst[i] = item
    #print '%s;%s;%s;%s' % (i, l, m, item)
for n in nst:
    print n
