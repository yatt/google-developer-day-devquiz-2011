import sys
filename = 'cal.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

inv={'U':'D','D':'U','L':'R','R':'L'}
lst = eval(open(filename).read())
for n in lst:
    print ''.join(inv[ch] for ch in n)
