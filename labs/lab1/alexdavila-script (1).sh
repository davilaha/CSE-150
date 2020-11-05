#!/bin/bash
for file in 'ls'
do
	numLines="$(wc -l)"
	for((i=2; i<=numLines; i++))
	do
		if (i $counter % 2 -eq 0) then
			echo "${file}: $($line)"
		fi
	done
done	
	
