#include<cstdio>
#include<cstdlib>
#include<cstring>
#include<vector>
#include<deque>
#include<map>
#include<string>
using namespace std;

const int U=0;
const int D=2;
const int L=1;
const int R=3;
const int N=4;
const char* REPR="ULDRN";
map<char, int> VAL;

char inverseOperation(char op)
{
    return (op + 2) % 4;
}

const char *SEQUENCE = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
map<char, int> NUMS;
char OPERATABLES[7][7][5][36];
char origs[5000][37];
int moveto[7][7][4];

class Pazzle
{
public:
    int h;
    int w;
    char *orig;
    char grid[6*6 + 1];
    vector<char> opHist;
    int zeroAt;
    
    Pazzle()
    {
    }
    Pazzle(const Pazzle &pz)
    {
        h = pz.h;
        w = pz.w;
        orig = pz.orig;
        strcpy(grid, pz.grid);
        opHist = pz.opHist;
        zeroAt = pz.zeroAt;
    }

    Pazzle(int height, int width, char* line)
    {
        h = height;
        w = width;

        orig = line;
        
        reset();
    }

    void reset()
    {
        strcpy(grid, orig);

/*
        // apply
        deque<char> seq;
        for (int i = 0; i < h*w - 1; i++)
        {
            char ch = SEQUENCE[i];
            if (strchr(grid, ch) == NULL)
                seq.push_back(ch);
        }
        for (int i = 0; i < h*w; i++)
            if (grid[i] == '=')
            {
                grid[i] = seq[0];
                seq.pop_front();
            }
*/
    
        opHist.clear();
        opHist.push_back(N);
        
        for (int i = 0; i < h*w; i++)
            if (grid[i] == '0')
            {
                zeroAt = i;
                break;
            }
    }
    
    void operate(int op, bool hist = true)
    {
        int z = zeroAt;
        int n = zeroAt + moveto[h][w][op];
        
        if (grid[n] == '=')
            throw exception();
        char swp = grid[n];
        grid[n] = grid[z];
        grid[z] = swp;
        
        zeroAt = n;
        
        if (hist)
            opHist.push_back(op);
    }
    
    void undo()
    {
        char op = opHist.back();
        opHist.pop_back();
        operate(inverseOperation(op), false);
    }
    
    char operatables()
    {
        //char o = OPERATABLES[h][w][opHist.back()][zeroAt];
        char o = 0;
        int i = zeroAt / w;
        int j = zeroAt % w;
//printf("before %d\n", o);
        if (i >   0 && grid[zeroAt-w] != '=' && opHist.back() != D) o |= (1 << U);
        if (i < h-1 && grid[zeroAt+w] != '=' && opHist.back() != U) o |= (1 << D);
        if (j >   0 && grid[zeroAt-1] != '=' && opHist.back() != R) o |= (1 << L);
        if (j < w-1 && grid[zeroAt+1] != '=' && opHist.back() != L) o |= (1 << R);
//printf("after  %d\n", o);
        return o;
    }

    bool isComplete()
    {
        if (grid[w*h-1] != '0')
            return false;
        for (int i = 0; i < h*w-1; i++)
            if (grid[i] != SEQUENCE[i] && grid[i] != '=')
                return false;
        return true;
    }

    string operations()
    {
        string s = "";
        for (int i = 1; i < opHist.size(); i++)
            s = s + REPR[opHist[i]];
        return s;
    }
    
    int lowerbound()
    {
        int s = 0;
        char gij;
        int m, ox, oy, n, ex, ey;
        for (int i = 0; i < h; i++)
            for (int j = 0; j < w; j++)
            {
                gij = grid[i*w + j];
                if (gij == '0')
                    continue;
                
                m = i*w + j;
                ox = m / w;
                oy = m % w;
                
                n = NUMS[gij];
                ex = n / w;
                ey = n % w;
                
                s += abs(ex - ox) + abs(ey - oy);
            }
        return s;
    }
    
    int eval()
    {
        return lowerbound();
    }
    
    string serialize()
    {
        string s(grid);
        return s;
    }
    
    string toString() const
    {
        string s = "";
        for (int i = 0; i < h*w; i++)
        {
            if (i && i % w == 0)
                s += '\n';
            s += grid[i];
        }
        return s;
    }

    string ope()
    {
        char ops = operatables();
        string s = "";
        for (int i = 0; i < 4; i++)
            s = s + REPR[i] + ":" + (((ops>>i)&1)?"yes":"no") + " ";
        return s;
    }

    bool operator==(const Pazzle& p) const 
    {
        return strcmp(grid, p.grid) == 0;
    }
};

void _opable(int h, int w, int preop, int i, int j)
{
    char *p = &(OPERATABLES[h][w][preop][i*w+j]);
    *p = 0;
    if (i >   0 && preop != D) *p |= 1 << U;
    if (i < h-1 && preop != U) *p |= 1 << D;
    if (j >   0 && preop != R) *p |= 1 << L;
    if (j < w-1 && preop != L) *p |= 1 << R;
//if (h==3&&w==4)printf("%d,%d at %d,%d, op=%c => %d%d%d%d\n", h, w, i, j, REPR[preop], (*p >> 0) & 1, (*p >> 1) & 1,(*p >> 2) & 1,(*p >> 3) & 1 );
}

void pazzleInit()
{
    // VAL
    VAL['U'] = U;
    VAL['D'] = D;
    VAL['L'] = L;
    VAL['R'] = R;

    // operatables
    for (int h = 3; h <= 6; h++)
        for (int w = 3; w <= 6; w++)
            for (int preop = 0; preop < 5; preop++)
                for (int i = 0; i < h; i++)
                    for (int j = 0; j < w; j++)
                        _opable(h, w, preop, i, j);

    // lowerbound
    
    // nums
    for (int i = 0; SEQUENCE[i] != '\0'; i++)
        NUMS[SEQUENCE[i]] = i;
    
    // moveto
    for (int h = 3; h <= 6; h++)
        for (int w = 3; w <= 6; w++)
        {
            moveto[h][w][0] = -w;
            moveto[h][w][1] = -1;
            moveto[h][w][2] = +w;
            moveto[h][w][3] = +1;
        }
}


vector<Pazzle> readfromfile()
{
    vector<Pazzle> ps;
    int n;
    int lms[4];
    int h, w; 
    char buf[1000];
    
    FILE *fp = fopen("problems.txt", "r");
    int r = fscanf(fp, "%d %d %d %d %d ", lms, lms + 1, lms + 2, lms + 3, &n);
    for (int i = 0; i < 5000; i++)
    {
        int s = fscanf(fp, "%d,%d,%s", &w, &h, buf);
        strcpy(origs[i], buf);
        Pazzle p(h, w, origs[i]);
        ps.push_back(p);
    }
    return ps;
}

