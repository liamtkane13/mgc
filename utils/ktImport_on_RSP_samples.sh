#!/usr/bin/env bash

for `i in ls *16gb*krona | cut -f 1 -d '-'`;
do
printf ${i}\n
done