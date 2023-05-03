#!/usr/bin/env bash

for i in `ls *16gb*krona | cut -f 1 -d '-'`;
do
ktImportText ${i}*16gb*krona -o ${i}-kraken.html
aws s3 cp ${i}-kraken.html s3://mgc-minion/mgc_qc/kraken/
rm ${i}-kraken.html
done