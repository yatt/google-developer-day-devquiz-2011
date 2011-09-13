#include<iostream>
#include<vector>
#include"Pazzle.cpp"
char cal[5000][400];
int main()
{
    vector<Pazzle> ps = readfromfile();
    FILE *fp = fopen("submit.txt", "r");
    int nInvalid = 0;
    for (int i = 0; i < 5000; i++)
    {
        if (!strcmp(cal[i], ""))
            continue;
        for (int j = 0; cal[i][j] != '\0'; j++)
            ps[i].operate(VAL[cal[i][j]]);
        if (!ps[i].isComplete())
        {
            printf("error: Problem No=%d\n", i+1);
            cout << ps[i].toString() << endl;
            nInvalid++;
        }
    }
    printf("%d errors.\n", nInvalid);
    return 0 ;
}
