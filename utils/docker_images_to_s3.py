#!/usr/bin/env python3

import os
import glob
from datetime import date
import subprocess

def docker_pull(files):
    
    container_list = []

    for file in files:
        with open(file, 'r') as file:
            for line in file:
                if 'container' in line:
                    line = line.lstrip()
                    if line.startswith('//'):
                        continue
                    else:
                        line = line.split("'")[1]
                        if line not in container_list:
                            container_list.append(line)

    for i in container_list:
        command = (f'docker pull {i}')
        os.system(command)

    return container_list    


def docker_save(containers):
    docker_image_subdir='docker-image-backup'
    if not os.path.exists(docker_image_subdir):
        os.makedirs(docker_image_subdir)
    for i in containers:
        cmd= ""
        if '/' in i:
            directory = i.split('/')[0]
            if not os.path.exists(f'{docker_image_subdir}/{directory}'):
                os.makedirs(f'{docker_image_subdir}/{directory}')
            name = i.split('/')[1]
            cmd=(f'docker save {i} | gzip -c > {docker_image_subdir}/{directory}/{name}.tar.gz')
        else:
            name = i
            cmd=(f'docker save {i} | gzip -c > {docker_image_subdir}/{name}.tar.gz')
        os.system(cmd)


def README():
    git_hash_command = ('git rev-parse HEAD')
    commit_hash_encoded = subprocess.check_output(['bash', '-c', git_hash_command])
    commit_hash = commit_hash_encoded.decode('utf8')

    git_branch_command = ('git rev-parse --abbrev-ref HEAD')
    branch_encoded = subprocess.check_output(['bash', '-c', git_branch_command])
    git_branch= branch_encoded.decode('utf8')

    description = 'This script parses through all nextflow files in the /nextflow/ git directory, extracts all Docker containers used in nextflow scripts, and makes backup tar files of each Docker image.'

    todays_date = date.today()

    with open('README.txt', 'w') as outfile:

        outfile.write(f'README file for docker_images_to_s3.py\n')
        outfile.write(f'\n{description}\n')
        outfile.write(f'\nThe last backup occurred on:\n{todays_date}\n')
        outfile.write(f'\nThe Github commit branch is:\n{git_branch}')
        outfile.write(f'\nThe Github commit hash is:\n{commit_hash}')
        outfile.close()
        

def main():
    nextflow_files = '/Users/liamkane/software/mgc/nextflow/*.nf'
    nextflow_files = glob.glob(nextflow_files)
    container_list = docker_pull(nextflow_files)
    docker_save(container_list)
    README()

if __name__ == "__main__":
    main()
