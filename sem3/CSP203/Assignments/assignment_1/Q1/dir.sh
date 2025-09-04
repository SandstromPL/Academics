#!/bin/bash

echo Enter the file name :
read file

while IFS=":" read -r name department type; do
	mkdir -p "$type/$department/$name"
done < $file
