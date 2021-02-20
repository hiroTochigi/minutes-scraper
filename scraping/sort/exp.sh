#!/bin/bash
uniq -c < street_list.txt >> count_street_list
input="count_street_list"
echo "street_list = [" >> temp_street_list_val.txt
while IFS= read -r line
do
  num=$(echo "$line"| awk '{print NF}')
  if [ $num -eq 3 ]; then
    echo "$line" | awk '{ print "\t\""$2"\"," }' >> temp_street_list_val.txt
  elif [ $num -eq 4 ]; then
    echo "$line" | awk '{ print "\t\"" $3 " " $4 "\"," }' >> temp_street_list_val.txt
  elif [ $num -eq 5 ]; then
    echo "$line" | awk '{ print "\t\""$2" "$3" "$4"\","}' >> temp_street_list_val.txt
  elif [ $num -eq 6 ]; then
    echo "$line" | awk '{ print "\t\""$2" "$3" "$4" "$5"\"," }' >> temp_street_list_val.txt
  fi
done < "$input"
echo "]" >> temp_street_list_val.txt

