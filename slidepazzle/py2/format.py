import sys
filename = 'cal.txt'
if len(sys.argv) > 1:
    filename = sys.argv[1]

for n in eval(open(filename).read()):
    print n
