if [ $# -ne 1 ]; 
then
    echo " $0 <n>"
    exit 1
fi
n=$1
if [ $n -lt 0 ]; then
    echo "enter valid input:"
    exit 1
fi
a=0
b=1

for ((i=2; i<=n; i++))
do
    fib=$((a + b))
    a=$b
    b=$fib
done

if [ $n -eq 0 ]; then
    fib=0
elif [ $n -eq 1 ]; then
    fib=1
fi

echo "Fibonacci of $n is $fib"
