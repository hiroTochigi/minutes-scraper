#!/bin/sh
# My first Script
echo "Hello World!"
echo "Test" >>  test_file2.txt
while IFS= read -r line;do
    echo "$line" >> test_file2.txt
done < "rwexp.sh"
echo "completed"
