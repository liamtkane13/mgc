#!/usr/bin/env bash 

# qualimap-target.sh

for i in `cat test.txt`;
do 
aws s3 cp s3://mgcdata/SS2/bams/public/${i}.bam .
mkdir ${i}/
echo 'Running QualiMap on ${i}'
echo 'qualimap --java-mem-size=6G bamqc -bam ${i}.bam -outdir ${i}/ -outfmt HTML -nt 2 --feature-file Agilent-v3-Covered-04-01-2022.bed'	
echo 'aws s3 cp ${i}/ s3://mgcdata/SS2/qualimap/${i}/'
done 