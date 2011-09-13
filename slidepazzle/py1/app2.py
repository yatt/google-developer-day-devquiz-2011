# coding: utf-8
try:
    import pscyo; psyco.full()
except:
    pass
MAXHEIGHT = 4
MAXWIDTH  = 4
MAXDEPTH  = 20
# 3 4 20
# 6 6 10
# 4 4 20


def fn(h, w, d):
    g = [[None for j in range(w)] for i in range(h)]
    for x in range(h):
        for y in range(w):
            lst = ['U', 'D', 'L', 'R']
            if x == 0:
                lst.remove('D')
            if x == h - 1:
                lst.remove('U')
            if y == 0:
                lst.remove('R')
            if y == w - 1:
                lst.remove('L')
            try:
                INVERSE = {'U':'D', 'D':'U', 'L':'R', 'R':'L', '':''}
                lst.remove(INVERSE[d])
            except: pass
            g[x][y] = lst
    return g

def gn():
    operatables = {}
    for h in range(3, 7):
        for w in range(3, 7):
            operatables[(h, w)] = {}
            for d in 'UDLR':
                operatables[(h, w)][d] = fn(h, w, d)
            operatables[(h, w)][''] = fn(h, w, '')
    return operatables
# ops = gn()
# ops[(w,h)][pre][i][j]

def pn():
    movefrom = {}
    diff = {
        'U': (+1, +0), 'D': (-1, +0),
        'L': (+0, +1), 'R': (+0, -1),
    }
    for x in range(6):
        for y in range(6):
            movefrom[(x, y)] = {}
            for d in 'UDLR':
                s = x + diff[d][0]
                t = y + diff[d][1]
                movefrom[(x, y)][d] = (s, t)
    return movefrom

            
class Pazzle:
    UP='U'
    DOWN='D'
    LEFT='L'
    RIGHT='R'
    SEQUENCE='123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    INVERSE = {'U':'D', 'D':'U', 'L':'R', 'R':'L'}
    OPERATABLES = gn()
    MOVETO = pn()
    def __init__(self, w, h, line):
        self.width = w
        self.height = h
        self.ops = Pazzle.OPERATABLES[(self.height, self.width)]
        self.orig = line
        self.reset()
    
    def emptyPoint(self):
        # index of '0'
        i = ''.join(''.join(row) for row in self.grid).index('0')
        x = i // self.width
        y = i % self.width
        return x,y
    
    def operate(self, op, hist=True):
        x,y = self.zeroat
        s,t = Pazzle.MOVETO[self.zeroat][op]
        #if s < 0 or s >= self.height or t < 0 or t >= self.width:
        #    print 'wrong!',x,y,op,s,t
        self.grid[x][y], self.grid[s][t] = self.grid[s][t], self.grid[x][y]
        self.zeroat = (s, t)
        if hist:
            self.ophist.append(op)

    def undo(self):
        op = self.ophist.pop()
        self.operate(Pazzle.INVERSE[op], False)
    
    def reset(self):
        # reset initial state
        self.grid = [[self.orig[i*self.width+j] for j in range(self.width)] for i in range(self.height)]
        self.ophist = ['']
        self.zeroat = self.emptyPoint()
        
    def operatables(self):
        x,y = self.zeroat
        return self.ops[self.ophist[-1]][x][y]

    def isComplete(self):
        if self.grid[self.height-1][self.width-1] != '0':
            return False
        for i in range(self.height):
            for j in range(self.width - (0 if i != self.height - 1 else 1)):
                ch = self.grid[i][j]
                if ch != Pazzle.SEQUENCE[i*self.width+j] and ch != '=':
                    return False
        return True

    def __repr__(self):
        return '\n'.join(''.join(row).replace('0', '@') for row in self.grid)
    
    def toOperationList(self):
        return ''.join(''.join(row) for row in self.ophist)

    def serialize(self):
        # ハッシュにしちゃうという手もありか？情報落ちすぎると困るけど
        return ''.join(''.join(row) for row in self.grid)


def readfromfile():
    ifs = open('problems.txt')
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
# pazzle = p かつ d < depth の場合のみ枝狩りできる
visited = set()  # 枝狩りに使う
maxdepth = MAXDEPTH # 探索する最大深さ
minop = ''      # 最短手数の命令リスト
lenminop = 99999 # len(minop)
answers = []     # 回答すべて
def recursion(pazzle, maxdepth, depth = 1):
    global minop, lenminop
    
    s = pazzle.serialize()
    for d in range(depth, maxdepth+1):visited.add(s + str(d))
    
    for op in pazzle.operatables():
        pazzle.operate(op)
        
        #if not pazzle.isComplete() and (depth, pazzle.serialize()) in visited:
        #    print 'detect',depth,pazzle.serialize()
        if pazzle.isComplete(): # one answer found
            oplst = ''.join(pazzle.ophist)
            #answers.append(oplst)
            if len(oplst) < lenminop:
                minop = oplst
                lenminop = len(minop)
        elif depth < maxdepth and \
             depth <= lenminop and \
             not (pazzle.serialize() + str(depth) in visited):
            recursion(pazzle, maxdepth, depth + 1)
        pazzle.undo()


# 深さ優先の探索にすると初めに見つかる解がやたらと長くなる。
# これ幅優先とか反復深化探索で解こうとするとどうなるんだろう？


def trySolve(pazzle):
    global answers, minop, lenminop, visited
    answers = []
    minop = ''
    lenminop = 99999
    visited = set()
    recursion(pazzle, MAXDEPTH)
    return minop

def main():
    ofs = open('log.txt', 'w')
    cal = eval(open('cal.txt').read())

    limits,n,ps = readfromfile()
    #print limits,n
    nSuccess = 0
    for i,p in enumerate(ps):
        if cal[i] != '':
            print 'already solved',i+1
            continue
        #print i,
        #print i,p.height,p.width
        #print p
        if p.width <= MAXWIDTH and p.height <= MAXHEIGHT:
            oplst = trySolve(p)
            if oplst != '':
                nSuccess += 1
                print i+1,oplst
                cal[i] = oplst
                ofs.write("%d: %s\n" % (i+1, oplst))
            else:
                ofs.write("%d: skip\n" % (i+1))
        else:
            #print 'skip'
            ofs.write("%d: skip\n" % (i+1))
        ofs.flush()
    ofs.write('solved %s problems.\n' % nSuccess)
    ofs.close()
    
    ofs = open('cal.txt', 'w')
    ofs.write(repr(cal))
    ofs.close()

        
if __name__ == '__main__':
    main()
