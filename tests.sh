for word in `cat badwords.txt` do
    grep $word chapter* && exit 1
done
print "No bad words"