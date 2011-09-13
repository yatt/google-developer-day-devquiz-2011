# coding: utf-8
import app2
import collections

lm,n,ps = app2.readfromfile()
lst = eval(open('cal.txt').read())

d = collections.defaultdict(int)
e = collections.defaultdict(int)
for i,p in enumerate(ps):
    d[(p.height, p.width)] += 1
    if lst[i] != '':
        e[(p.height, p.width)] += 1

s = 0
print 'h w prob  sum  pnt nsol'
print '-----------------------'
for k in sorted(d):
    s += d[k]
    print '%d %d %4d %4d %4d %4d' % (k[0], k[1], d[k], s, s // 100, e[k])


# 解いた問題
solved = sum(1 for item in eval(open('cal.txt').read()) if item != '')
print
print 'solved %d problems.' % (solved)

# 使用文字数
d = {'U': 0, 'D': 0, 'L': 0, 'R': 0}
for path in lst:
    for ch in path:
        d[ch] += 1
limits = map(int, open('problems.txt').readline().split())
print
print limits
print d['L'],d['R'],d['U'],d['D']
# 2011/09/09 22:52  3x3 全部とけた

