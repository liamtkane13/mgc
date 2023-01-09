#!/usr/bin/env bash 

# qualimap-target.sh

for i in `cat test.txt`;
do 
aws s3 cp s3://mgcdata/SS2/bams/public/${i}.bam .	
echo $i
done 