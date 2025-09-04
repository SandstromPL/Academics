if [ $# -ne 1 ]; 
then
    echo "Usage: $0 <file.c>"
    exit 1
fi
file=$1
keywords="char int unsigned main void switch float for else"
for i in $keywords; do
    count=$(grep -o -w $i $file | wc -l)
    echo "$i: $count"
done
