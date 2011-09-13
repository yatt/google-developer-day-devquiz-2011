# coding: utf-8
try:
    import psyco
    psyco.full()
    print '=== psyco enabled ==='
except:
    pass
    

class Pazzle:
    UP='U'
    DOWN='D'
    LEFT='L'
    RIGHT='R'
    SEQUENCE='123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def __init__(self, w, h, line):
        self.width = w
        self.height = h
        self.orig = line
        self.opdir = {
                    Pazzle.UP  : (+1, +0), Pazzle.DOWN : (-1, +0),
                    Pazzle.LEFT: (+0, +1), Pazzle.RIGHT: (+0, -1),
                    }
        self.invop = {
                    Pazzle.UP  : Pazzle.DOWN , Pazzle.DOWN : Pazzle.UP  ,
                    Pazzle.LEFT: Pazzle.RIGHT, Pazzle.RIGHT: Pazzle.LEFT,
                    }
        self.reset()
    
    def emptyPoint(self):
        # index of '0'
        i = ''.join(''.join(row) for row in self.grid).index('0')
        x = i // self.width
        y = i % self.width
        return x,y
    
    def operate(self, op, hist=True):
        x,y = self.zeroat
        s,t = x + self.opdir[op][0], y + self.opdir[op][1]
        if s < 0 or self.height <= s or t < 0 or self.width <= t:
            raise Exception('%d,%d <-> %d,%d op:%s \n%s' % (x, y, s, t, op, self))
        self.grid[x][y], self.grid[s][t] = self.grid[s][t], self.grid[x][y]
        self.zeroat = (s, t)
        if hist:
            self.ophist.append(op)

    def undo(self):
        op = self.ophist.pop()
        self.operate(self.invop[op], False)
    
    def reset(self):
        # reset initial state
        self.grid = [[self.orig[i*self.width+j] for j in range(self.width)] for i in range(self.height)]
        self.ophist = []
        self.zeroat = self.emptyPoint()
        
    def operatables(self):
        # available operations
        lst = [Pazzle.UP, Pazzle.DOWN, Pazzle.LEFT, Pazzle.RIGHT]
        x,y = self.emptyPoint()
        if x == 0:
            lst.remove(Pazzle.DOWN)
        if x == self.height - 1:
            lst.remove(Pazzle.UP)
        if y == 0:
            lst.remove(Pazzle.RIGHT)
        if y == self.width - 1:
            lst.remove(Pazzle.LEFT)
        try:
            lst.remove(self.invop[self.ophist[-1]])
        except: pass
        
        return lst

    def isComplete(self):
        if self.grid[self.height-1][self.width-1] != '0':
            return False
        for i in range(self.height):
            for j in range(self.width - (0 if i != self.height - 1 else 1)):
                ch = self.grid[i][j]
                if ch != '=' and ch != Pazzle.SEQUENCE[i*self.width+j]:
                    return False
        return True

    def __repr__(self):
        return '\n'.join(''.join(row).replace('0', '@') for row in self.grid)
    
    def serialize(self):
        # ハッシュにしちゃうという手もありか？情報落ちすぎると困るけど
        return ''.join(''.join(row) for row in self.grid)


def readfromfile():
    ifs = open('problems.txt')
    #ifs = open('test.txt')
    #ifs = open('test2.txt')
    #ifs = open('test3.txt')
    limits = map(int, ifs.readline().split())
    n = int(ifs.readline())
    
    ps = []
    for line in ifs:
        line = line.split(',')
        w = int(line[0])
        h = int(line[1])
        g = line[2].strip()
        ps.append(Pazzle(w, h, g))

    ifs.close()
    return limits,n,ps


# なんか、やっぱりVB.NETとかC#とかと比べるとデバッグに時間かかるし、
# 編集するときに補完がかからないのが面倒だ。
# ただファイル操作とか文字列の操作がかなり楽なんだよなぁ
#
# 変数名の変更とかだるいし


# ループの検出とかやればもっと早くなるはず
# 要するに枝狩り
# 過去に探索した状態を保存しておけばループ検出が可能になるな
# メモリすごい食いそうだ
#
# あ、こう簡単にはできないか。同じ状態でもdepthが違えば
# もっと先まで探索できるかもしれないもんな。
# (depth, pazzle)のペアがあって、(d,p)が現在の状態なら、
# pazzle = p かつ d < depth の場合のみ枝狩り可能だ。
#
# じゃあsetじゃなくて{key:pazzle, val:depth}のデータ構造じゃないといけないのか。
# ん？ちがう？
visited = set()
maxdepth = 20
minop = ' '
lenminop = 99999
answers = []
def recursion(pazzle, depth = 1):
    global minop, lenminop
    #visited.add((depth, pazzle.serialize()))
    for op in pazzle.operatables():
        try:
            pazzle.operate(op)
        except Exception, e:
            import code
            code.InteractiveConsole(locals()).interact()
            raise e
        if pazzle.isComplete():
            oplst = ''.join(pazzle.ophist)
            print '== complete!!', oplst
            answers.append(oplst)
            if len(oplst) < lenminop:
                minop = oplst
                lenminop = len(minop)
        elif depth < maxdepth and \
             depth <= lenminop and \
             not ((depth, pazzle.serialize()) in visited):
            recursion(pazzle, depth + 1)
        elif pazzle.serialize() in visited:
            #print 'detected!', pazzle.serialize()
            pass
        pazzle.undo()


def trySolve(pazzle):
    global answers, minop, lenminop
    answers = []
    minop = ' '
    lenminop = 99999
    recursion(pazzle)
    return minop

def main():
    limits,n,ps = readfromfile()
    
    print limits,n
    #try:
    #    print ps[0]
    #    ps[0].operation(Pazzle.DOWN)
    #    ps[0].operation(Pazzle.DOWN)
    #except Exception, e:
    #    print e
    #finally:
    #    pass
    
    #print ps[0]
    #print ps[0].operatables()
    #ps[0].operate(Pazzle.DOWN)
    #print 
    #print ps[0]
    #print ps[0].operatables()
    
    #import random
    #p = ps[0]
    #while True:
    #    ops = p.operatables()
    #    op = random.choice(ops)
    #    print ops
    #    print op
    #    p.operate(op)
    #    print p
    #    print
    #    import time
    #    time.sleep(1)
    
    #testx()
    
    #r = trySolve(ps[0])
    #if r is None:
    #    print 'answer if not found.'
    #else:
    #    print '<<<<<<<found!>>>>>>>'
    #    print 'op list:',''.join(ps[0].ophist)
    
    for p in ps:
        print trySolve(p)
        
    

def testx():
    p = Pazzle(3, 3, '041853276')
    for op in 'LUURDLURDLDLURLURDRD':
        p.operate(op)
    print p
    print p.operatables()

    
if __name__ == '__main__':
    main()
