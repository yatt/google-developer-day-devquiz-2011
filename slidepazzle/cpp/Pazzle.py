# coding: utf-8
import array
import string

U=0
D=2
L=1
R=3 # 逆操作は(OP + 2) % 4
N=4 # 前操作が何もない場合
REPR='ULDR'
OPS={'U':U,'D':D,'L':L,'R':R}
SEQUENCE='123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMS = dict(zip(SEQUENCE, range(len(SEQUENCE))))

def xn(ops):
    return [REPR[op] for op in ops]

def inverseOperation(op):
    return (op + 2) % 4

def fn(h, w, preop):
    g = [None for i in range(h*w)]
    for x in range(h):
        for y in range(w):
            lst = [U, D, L, R]
            if x == 0:
                lst.remove(U)
            if x == h - 1:
                lst.remove(D)
            if y == 0:
                lst.remove(L)
            if y == w - 1:
                lst.remove(R)
            
            if preop != N:
                inv = inverseOperation(preop)
                try:
                    lst.remove(inv)
                except: pass
            
            g[x*w + y] = lst
    return g

def gn():
    operatables = {}
    for h in range(3, 7):
        operatables[h] = {}
        for w in range(3, 7):
            operatables[h][w] = {}
            for d in [U, D, L, R, N]:
                operatables[h][w][d] = fn(h, w, d)
    return operatables


def lbound():
    lowerbound = {}
    for h in range(3, 7):
        lowerbound[h] = {}
        for w in range(3, 7):
            lowerbound[h][w] = {}
            for i in range(h):
                lowerbound[h][w][i] = {}
                for j in range(w):
                    lowerbound[h][w][i][j] = {}
                    m = i*w + j
                    ox,oy = m // w, m % w
                    for c in SEQUENCE:
                        n = NUMS[c]
                        ex,ey = n // w, n % w
                        
                        n = abs(ex - ox) + abs(ey - oy)
                        
                        lowerbound[h][w][i][j][c] = n
    return lowerbound
 
def mn():
    #self.moveto = [-w, -1, +w, +1] # ULDR
    return [[(-w, -1, +w, +1) for w in range(7)] for h in range(7)]

OPERATABLES = gn()
LOWERBOUNDS = lbound()
MOVETO      = mn()
class Pazzle:
    def __init__(self, w, h, line):
        self.width = w
        self.height = h
        self.ops = OPERATABLES[h][w]
        self.lbs = LOWERBOUNDS[h][w]
        self.orig = line
        self.reset()
    
    def reset(self):
        self.grid = array.array('c', self.orig)
        # '='には、足りない文字を適当に割り当ててしまう
        # lowerboundによる枝刈りで有利にするため。
        seq = SEQUENCE[:self.height * self.width - 1]
        seq = [ch for ch in seq if ch not in self.grid]
        for i in range(len(self.grid)):
            if self.grid[i] == '=':
                self.grid[i] = seq.pop()
        self.opHist = array.array('B', [N])
        self.zeroAt = self.grid.index('0')
        self.mlowerbound = self._lowerbound()
    
    def operate(self, op, hist=True):
        z = self.zeroAt
        n = self.zeroAt + MOVETO[self.height][self.width][op]
        g = self.grid
        if g[n] == '=':
            raise Exception()
        #if g[z] != '=':
        #    self.mlowerbound 
        #    num = NUM[g[z]]
        #    x,y = num // self.width, num % self.width
        #    s,t = z   // self.width, z   % self.width
        #    l,m = n   // self.width, n   % self.width
        #    if abs(s - x) + abs(t - y) - abs(l - x) - abs(m - y) > 0:
        #        self.mlowerbound += 1
        g[n],g[z] = g[z],g[n]
        self.zeroAt = n
        if hist:
            self.opHist.append(op)

    def undo(self):
        op = self.opHist.pop()
        self.operate(inverseOperation(op), False)
        
    def operatables(self):
        return self.ops[self.opHist[-1]][self.zeroAt]

    def isComplete(self):
        if self.grid[-1] != '0':
            return False
        for i in range(len(self.grid) - 1):
            ch = self.grid[i]
            if ch != SEQUENCE[i] and ch != '=':
                return False
        return True

    def __repr__(self):
        h = self.height
        w = self.width
        return '\n'.join(''.join(self.grid[i*w+j] for j in range(w)) for i in range(h))
    
    def serialize(self):
        return self.grid.tostring()
    
    def operations(self):
        a = 'ULDR'
        return ''.join(a[self.opHist[i]] for i in range(1, len(self.opHist)))
    
    def lowerbound(self):
        return self._lowerbound()
        return self.mlowerbound
    
    def _lowerbound(self):
        # 下限値; 最低限必要な手数の合計数
        s = 0
        h = self.height
        w = self.width
        for i in range(h):
            for j in range(w):
                gij = self.grid[i*w + j]
                if gij == '0':
                    continue
                
                #m = i*w + j
                #ox,oy = m // w, m % w
                #
                #n = NUMS[self.grid[i*w + j]]
                #ex,ey = n // w, n % w

                #s += abs(ex - ox) + abs(ey - oy)
                s += self.lbs[i][j][gij]

        return s

    def eval(self):
        # 評価関数
        return self.lowerbound()
        

        s = 0
        h = self.height
        w = self.width
        for i in range(h):
            for j in range(w):
                if self.grid[i*w + j] == SEQUENCE[i*w + j]:
                    s += 1 * ((h - i + 1) + (w - j + 1))
        return s
        
        # 左上の駒の下限値が低いほど高得点になる
        s = 0
        h = self.height
        w = self.width
        for i in range(h):
            for j in range(w):
                gij = self.grid[i*w + j]
                if gij == '0':
                    continue
                #s += ((h - i) + (w - j)) * (h*w - self.lbs[i][j][gij])
                s += 3.0 / (((h - i + 1) + (w - j + 1)) * (self.lbs[i][j][gij])+1)
        return s


                   
                    


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
