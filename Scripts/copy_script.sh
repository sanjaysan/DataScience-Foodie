#! /bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    rm -rf ../Data/text/$line
done < "$1"           
