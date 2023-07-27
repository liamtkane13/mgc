#!/usr/bin/env bash

mkdir ~/software/cronjob/
cd ~/software/cronjob/ && nextflow ~/software/mgc/nextflow/mongo_backup.nf
ch ~/software/ && rm -rf cronjob/