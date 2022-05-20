#!/usr/bin/env python3

# pull_s3_qualimap.py

import subprocess

def make_accession_files():
    todo_public_bam_process = (f'aws s3 ls s3://mgcdata/SS2/bams/public/ > todo_bam_list.txt')
    todo_private_bam_process = (f'aws s3 ls s3://mgcdata/SS2/bams/private/ >> todo_bam_list.txt')
    done_bam_process = (f'aws s3 ls s3://mgcdata/SS2/qualimap/ > done_bam_list.txt')
    subprocess.check_output(['bash', '-c', todo_public_bam_process])
    subprocess.check_output(['bash', '-c', todo_private_bam_process])
    subprocess.check_output(['bash', '-c', done_bam_process])


def make_rsp_list():

    bam_list = []
    finished_bam_list = []
    todo_bam_list = []

    with open('done_bam_list.txt') as file1:
        for line in file1:
            tag = line.split(' ')[-1:]
            for x in tag:
                finished_tag = x.strip('/\n')
                finished_bam_list.append(finished_tag)

    with open('todo_bam_list.txt') as file:
        for line in file:
            if "bai" in line:
                continue
            else:
                bam_info = line.split(' ')
                for i in bam_info:
                    if "bam" in i:
                        it = i.strip('.bam\n')
                        bam_list.append(it)
    todo_bam_list = list(set(bam_list)^set(finished_bam_list))
    
    return todo_bam_list

def run_qualimap(sample_list):

    for i in sample_list:

        download_process = (f'aws s3 cp s3://mgcdata/SS2/bams/public/{i}.bam .') 
        subprocess.check_output(['bash', '-c', download_process])

        qualimap_process = (f'qualimap bamqc -bam {i}.bam -outdir {i} -outformat HTML -nt 8')
        subprocess.check_output(['bash', '-c', qualimap_process])

        sync_process = (f'aws s3 sync {i} s3://mgcdata/SS2/qualimap/')
        subprocess.check_output(['bash', '-c', sync_process])

        delete_process = (f'rm {i}*')
        subprocess.check_output(['bash', '-c', delete_process])


        print('quit')
        quit()

        


def main():
    make_accession_files()
    todo_bam_list = make_rsp_list()
    run_qualimap(todo_bam_list)



if __name__ == "__main__":
    main()
