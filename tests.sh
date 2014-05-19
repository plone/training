for word in `cat badwords.txt`
do
    grep $word *.rst && exit 1
done
exit 0
