#!/bin/bash

count=0

for i in {2000..7500}; do
	if echo "$i" | grep -q "4"; then
		count=$((count + 1))
		echo "$i"
	fi
done

echo "Total count of numbers containing digit 4 : $count"
