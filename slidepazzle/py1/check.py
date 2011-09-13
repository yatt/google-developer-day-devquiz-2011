import app2

limits,n,ps = app2.readfromfile()

for i,seq in enumerate(eval(open('cal.txt').read())):
    if seq == '':
        continue
    for ch in seq:
        ps[i].operate(ch)
    if not ps[i].isComplete():
        print 'error: Problem No=%d' % (i+1)
        
