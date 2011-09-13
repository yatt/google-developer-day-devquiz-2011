# coding: utf-8
import array

U=0
D=2
L=1
R=3 # 逆操作は(OP + 2) % 4
N=4 # 前操作が何もない場合
REPR='ULDR'
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


OPERATABLES = gn()
class Pazzle:
    def __init__(self, w, h, line):
        self.width = w
        self.height = h
        self.ops = OPERATABLES[h][w]
        #self.moveto = {U: -w, D: +w, L: -1, R: +1}
        self.moveto = [-w, -1, +w, +1] # ULDR
        self.orig = line
        self.grid = array.array('c', line)
        self.opHist = array.array('B', [N])
        self.zeroAt = self.grid.index('0')
    
    def operate(self, op, hist=True):
        z = self.zeroAt
        n = self.zeroAt + self.moveto[op]
        g = self.grid
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
        # 下限値; 最低限必要な手数の合計数
        s = 0
        h = self.height
        w = self.width
        for i in range(h):
            for j in range(w):
                if self.grid[i*w + j] in '0=':
                    continue
                
                m = i*w + j
                ox,oy = m // w, m % w
                
                n = NUMS[self.grid[i*w + j]]
                ex,ey = n // w, n % w

                s += abs(ex - ox) + abs(ey - oy)
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

