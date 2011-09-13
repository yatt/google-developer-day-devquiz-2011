#include<vector>
#include<iostream>
#include<queue>
#include<algorithm>
#include"Pazzle.cpp"
using namespace std;

class QueueItem
{
public:
    Pazzle pazzle;
    int eval;
    int depth;
    QueueItem(const Pazzle& p, int e, int d) : pazzle(p), eval(e), depth(d)
    {
    }
    bool operator<(const QueueItem& x) const 
    {
        return eval < x.eval; // 0.176 // 0.4

        //return depth < x.depth; // 0.28 // 43
        
        //if (eval < x.eval) // 0.179 // 0.46
        //    return true;
        //if (eval == x.eval)
        //    return depth < x.depth;
        //return false;
    }
    bool operator>(const QueueItem& x) const
    {
        return !operator<(x);
    }
};

int maxdepth = 20;
priority_queue<QueueItem, vector<QueueItem>, greater<QueueItem> > *q;
map<string, int> *visitedDepth;

bool isCut(int depth, Pazzle pazzle)
{
    string key(pazzle.grid);
    map<string, int> &m = *visitedDepth;
    if (m.find(key) != m.end() && m[key] > depth)
        return false;
    if (depth + pazzle.lowerbound() > maxdepth)
        return true;
    return false;
}


string search(Pazzle& _pazzle)
{
    q->push(QueueItem(_pazzle, _pazzle.eval(), 1));
    while (q->size() > 0)
    {
        QueueItem item(q->top());
        int depth = item.depth;
        Pazzle &pazzle = item.pazzle;
        q->pop();
        
        string key(pazzle.grid);
        map<string, int> &m = *visitedDepth;
        if (m.find(key) != m.end() && m[key] > depth)
            m[key] = depth;

        char ops = pazzle.operatables();
        for (int op = 0; op < 4; op++)
        {
            if (!((ops >> op) & 1))
                continue;
            
            pazzle.operate(op);
            if (pazzle.isComplete())
{
//cout << pazzle.toString() << endl;
//cout << pazzle.ope() << endl
                return pazzle.operations();
}
            if (depth < maxdepth && !isCut(depth, pazzle))
            {
                q->push(QueueItem(pazzle, pazzle.eval(), depth + 1));
            }
            pazzle.undo();
        }
    }
    string s = "";
    return s;
}

string trySolve(Pazzle& pazzle)
{
    q = new priority_queue<QueueItem, vector<QueueItem>, greater<QueueItem> >();
    visitedDepth = new map<string, int>();
    string r = search(pazzle);
    delete q;
    delete visitedDepth;
    return r;
}

const char *ifilename = "hsubmit.txt";
const char *ofilename = "hsubmit.txt";
char cal[5000][400];
void deserialize()
{
    FILE *fp = fopen(ifilename, "r");
    if (!fp)
    {
        for (int i = 0; i < 5000; i++)
            cal[i][0] = '\0';
        return;
        fprintf(stderr, "deserialize: ERROR: file not found\n");
        exit(0);
    }
    for (int i = 0; i < 5000; i++)
    {
        char *p = fgets(cal[i], 999, fp);
        cal[i][strlen(cal[i]) - 1] = '\0';
    }
    fclose(fp);
}
void serialize()
{
    FILE *fp = fopen(ofilename, "w");
    if (!fp)
    {
        fprintf(stderr, "serialize: ERROR: file not found\n");
        exit(0);
    }
    for (int i = 0; i < 5000; i++)
    {
        fputs(cal[i], fp);
        fputc('\n', fp);
    }
    fclose(fp);
}
void serializeat(int index, string s)
{
    deserialize();
    strcpy(cal[index], s.c_str());
    FILE *fp = fopen(ofilename, "w");
    if (!fp)
    {
        fprintf(stderr, "serialize: ERROR: file not found\n");
        exit(0);
    }
    for (int i = 0; i < 5000; i++)
    {
        fputs(cal[i], fp);
        fputc('\n', fp);
    }
    fclose(fp);
}


int maxheight = 3;
int maxwidth  = 3;

int minindex = 1;
int maxindex = 5000;

int main(int argc, char** argv)
{
    if (argc > 1)
        maxheight = atoi((const char*)argv[1]);
    if (argc > 2)
        maxwidth = atoi((const char*)argv[2]);
    if (argc > 3)
        maxdepth = atoi((const char*)argv[3]);
    if (argc > 4)
        minindex = atoi((const char*)argv[4]);
    if (argc > 5)
        maxindex = atoi((const char*)argv[5]);
    if (argc > 6)
        ifilename = ofilename = argv[6];

cout << "======================================" << endl;
cout << "maxdepth :" << maxdepth << endl;
cout << "ifilename:" << ifilename << endl;
cout << "ofilename:" << ofilename << endl;
cout << "======================================" << endl;

    pazzleInit();
    vector<Pazzle> ps = readfromfile();

cout << "@ INITIALIZATION COMPLETE" << endl;
    
    deserialize();
    for (int i = minindex-1; i < maxindex; i++)
    {
//if (i != 6) continue;
//if (i != 2417)continue;
        Pazzle& p = ps[i];
//while (true)
//{
//    cout << p.toString() << endl;
//    cout << p.ope() << endl;
//    char c = getchar();
//    if (c != '\n')
//        p.operate(VAL[c]);
//}

//cout << p.h << endl;
//cout << p.w << endl;
//cout << p.toString() << endl;
//p.operate(U);

//p.operate(U);
//cout << p.ope() << endl;
//cout << p.h<< endl;
//cout << p.w<< endl;
//cout << p.zeroAt / p.w << endl;
//cout << p.zeroAt % p.w << endl;
//cout << REPR[p.opHist.back()] << endl;
//cout << p.operations() << endl;
//cout << p.toString() << endl;
//return 0;

//q = new priority_queue<QueueItem>();
//QueueItem item1(p, p.eval(), 1); //
//p.operate(U);
//cout << item1.pazzle.toString() << endl << endl;
//cout << p.toString() << endl<< endl;
//QueueItem item2(p, p.eval(), 2); //
//
//q->push(item1);
//q->push(item2);
//cout << (q->top()).pazzle.toString() << endl<< endl; q->pop();
//cout << (q->top()).pazzle.toString() << endl<< endl; q->pop();
//
//q->push(item2);
//QueueItem item3(q->top());
//cout << item3.pazzle.toString() << endl<< endl; q->pop();
//delete q;
//return 0;
//q = new priority_queue<QueueItem>();
//QueueItem item(p, p.eval(), 1);
//q->push(item);
//p.operate(U);
//Pazzle pz(p);
//cout << p.toString() << endl;
//QueueItem item2(pz, pz.eval(), 2);
//q->push(item2);
//
////item = q->top(); q->pop();
////cout << item.pazzle.toString() << endl;
////item2 = q->top(); q->pop();
////cout << item2.pazzle.toString() << endl;
//cout << (q->top()).pazzle.toString() << endl; q->pop();
//cout << (q->top()).pazzle.toString() << endl; q->pop();
//
//delete q;
//return 0;
        if (strcmp(cal[i], "") != 0)
        {
            printf("already solved %d\n", i+1);
            continue;
        }
        if (p.h <= maxheight && p.w <= maxwidth)
        {
            string oplst = trySolve(p);
//printf(" %d  result '%s'\n",i+1, oplst.c_str());
            if (oplst != "")
            {
                printf("%d %d %d %s\n", i+1, p.h, p.w, oplst.c_str());
                strcpy(cal[i], oplst.c_str());
                serializeat(i, oplst);
            }
        }
    }
    //serialize();
    
    return 0;
}
