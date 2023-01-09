#!/usr/bin/env bash 

# qualimap-target.sh

for i in `cat test.txt`;
do 
aws s3 cp s3://mgcdata/SS2/bams/public/${i}.bam .
mkdir ${i}/
echo "Running QualiMap on ${i}"
qualimap --java-mem-size=6G bamqc -bam ${i}.bam -outdir ${i}/ -outformat HTML -nt 2 --feature-file Agilent-v3-Covered-04-01-2022.bed	
aws s3 sync ${i}/ s3://mgcdata/SS2/qualimap/${i}/
rm -r ${i}*
done 