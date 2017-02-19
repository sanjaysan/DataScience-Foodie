#! /bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    cp ./text/$line ./TaggedFiles 
done < "$1"
