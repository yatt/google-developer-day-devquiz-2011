# coding: utf-8
# breadth-first-search

import sys
import copy
import Queue
import Pazzle

    
# 枝刈り
# ループ検出
# 最小残り手数が深さ以上

# =は前処理で、その添え字にあるべき文字に
# 置き換えるとlowerboundが最小になって
# うれしいのでは

# lowerbound最小のものから探索していく
# => かわんね。

# queueuじゃなくて優先順位付きキューで探索するのが良いのでは？
# lowerbound. そうすると、lowerboundが小さくなる方向に
# 横に行ったり縦に行ったり縦横無尽になる感じだよな

# 6 6 30
MAXDEPTH = 20 # 探索する最大深さ
queue = None  # queue
visited = set()

def isCut(depth, pazzle):
    key = '%s%04d' % (pazzle.serialize(), depth)
    if key in visited:
        return True
    if depth + pazzle.lowerbound() > MAXDEPTH:
        return True
    return False

def search(pazzle):
    queue.put((1, copy.deepcopy(pazzle)))
    while not queue.empty():
        depth, pazzle = queue.get()
        for d in range(depth, MAXDEPTH):
            visited.add('%s%04d' % (pazzle.serialize(), d))
        for op in pazzle.operatables():
            pazzle.operate(op)
            if pazzle.isComplete():
                return pazzle.operations()
            if depth < MAXDEPTH and not isCut(depth, pazzle):
                queue.put((depth + 1, copy.deepcopy(pazzle)))
            pazzle.undo()
    return ''


def trySolve(pazzle):
    global queue, visited
    queue = Queue.Queue()
    visited = set()
    r = search(pazzle)
    queue = None
    return r


def main():
    global MAXDEPTH
    MAXHEIGHT = 6
    MAXWIDTH  = 6
    ifilename = 'cal.txt'
    ofilename = 'cal.txt'
    cal = eval(open(ifilename).read())
    limits,n,ps = Pazzle.readfromfile()
    
    if len(sys.argv) > 1:
        MAXDEPTH = int(sys.argv[1])
    if len(sys.argv) > 2:
        ofilename = sys.argv[2]
    
    nSuccess = 0
    for i,p in enumerate(ps):
        if cal[i] != '':
            print 'already solved',i+1
            continue
        if p.height <= MAXHEIGHT and p.width <= MAXWIDTH:
            oplst = trySolve(p)
            if oplst != '':
                nSuccess += 1
                print i+1,p.height,p.width,oplst
                cal[i] = oplst
            else:
                print 'miss',i+1
                pass
    
    ofs = open(ofilename, 'w')
    ofs.write(repr(cal))
    ofs.close()

#def main():
#    global MAXDEPTH
#    l,n,ps = Pazzle.readfromfile()
#    if len(sys.argv) > 1:
#        MAXDEPTH = int(sys.argv[1])
#    for i,p in enumerate(ps):
#        print i+1, trySolve(p)
#

if __name__ == '__main__':
    main()
