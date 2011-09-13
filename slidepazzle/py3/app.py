# coding: utf-8
# breadth-first-search
# lowerboundによる優先順位付きキュー
# 山登り法とかいうらしい。実装して調べてから気が付いた。

# backtrack -> breadth first search -> priority queue -> planning(lowerbound) -> planning(visited)
# 127 -> 210 -> 300 -> 421 -> 

# =に数値を当てはめてMDを求める。深さ削れる。
# より浅い深さで既にvisitなら枝刈り
# opHistを2ビットの配列で持てばopHistのデータ1/4

# lowerboundでは場所によって点数が変わらないけど
# 左上のものほど評価として高いのではないか?

import sys
import copy
import gc
import Pazzle
import pqueue

    
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
# 6 6 35
MAXDEPTH = 20 # 探索する最大深さ
queue = None  # queue
visitedDepth = {}

def isCut(depth, pazzle):
    # より浅い階層で既に探索している（する予定がある）場合
    if visitedDepth.get(pazzle.serialize(), depth) < depth:
        return True
    # 現在の深さと下限値が最大探索深さを超える場合
    if depth + pazzle.lowerbound() > MAXDEPTH:
        return True
    return False

def search(pazzle):
    #queue.put((pazzle.eval(), 1, copy.deepcopy(pazzle)))
    queue.put((1, pazzle.eval(), copy.deepcopy(pazzle)))
    while not queue.empty():
        evl, depth, pazzle = queue.get()

        # より浅い階層だったなら更新
        key = pazzle.serialize()
        if visitedDepth.get(key, depth) > depth:
            visitedDepth[key] = depth

        for op in pazzle.operatables():
            pazzle.operate(op)
            if pazzle.isComplete():
                return pazzle.operations()
            if depth < MAXDEPTH and not isCut(depth, pazzle):
                #queue.put((pazzle.eval(), depth + 1, copy.deepcopy(pazzle)))
                queue.put((depth + 1, pazzle.eval(), copy.deepcopy(pazzle)))
            pazzle.undo()
    return ''


def trySolve(pazzle):
    global queue, visitedDepth
    queue = pqueue.PriorityQueue()
    visitedDepth = {}
    r = search(pazzle)
    queue = None
    gc.collect()
    return r


def main():
    global MAXDEPTH
    MAXHEIGHT = 3
    MAXWIDTH  = 3
    ifilename = 'ccal.txt'
    ofilename = 'ccal.txt'
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
                #print 'miss',i+1
                pass
    
    ofs = open(ofilename, 'w')
    ofs.write(repr(cal))
    ofs.close()

#def main():
#    global MAXDEPTH
#    l,n,ps = Pazzle.readfromfile()
#    if len(sys.argv) > 1:
#        MAXDEPTH = int(sys.argv[1])
#    trySolve(ps[6])
#    return
#    for i,p in enumerate(ps):
#        print i+1, trySolve(p)


if __name__ == '__main__':
    main()
