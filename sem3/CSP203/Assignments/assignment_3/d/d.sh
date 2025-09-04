#!/bin/bash

# File containing the sales data
input_file="company_sales_data.csv"

# Step 1: Calculate total sales for each product and find the top product
top_product=$(awk '
    NR > 1 {
        facecream+=$2;
        facewash+=$3;
        toothpaste+=$4;
        bathingsoap+=$5;
        shampoo+=$6;
        moisturizer+=$7;
    }
    END {
        print "facecream", facecream;
        print "facewash", facewash;
        print "toothpaste", toothpaste;
        print "bathingsoap", bathingsoap;
        print "shampoo", shampoo;
        print "moisturizer", moisturizer;
    }
' "$input_file" | sort -k2 -nr | head -n 1 | awk '{print $1}')

# Step 2: Find the column number for the top product and extract monthly data
col_num=$(awk -v product="$top_product" 'NR==1 {for (i=2; i<=NF; i++) if ($i==product) print i}' "$input_file")
awk -v col="$col_num" 'NR==1 {print "month_number", "'$top_product'"} NR>1 {print $1, $col}' "$input_file" > temp1.dat

echo "Top product data for $top_product saved in temp1.dat."
