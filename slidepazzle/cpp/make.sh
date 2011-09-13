OUT=submit.txt
python merge.py submit-1.txt submit-2.txt > tmp1.txt 2>/dev/null
python merge.py tmp1.txt submit-3.txt > tmp2.txt 2>/dev/null
python merge.py tmp2.txt submit-4.txt > tmp3.txt 2>/dev/null
python merge.py tmp3.txt submit-5.txt > tmp4.txt 2>/dev/null
python merge.py tmp4.txt submit-6.txt > $OUT 2>/dev/null

rm tmp?.txt

N=$(sort submit.txt | uniq | wc -l)
N=$(expr $N - 1)
echo '============================'
echo 'solved' $N 'problems'
echo '============================'

SRC=src.zip
zip $SRC Pazzle.cpp app.cpp make.sh merge.py >/dev/null
echo 'create src archive' $SRC
echo 'create submit text' $OUT
