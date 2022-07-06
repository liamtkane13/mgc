#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
       Mandatory arguments:
           --fastq          FASTQ files to be Assembled
           --out_file       Output File            
    """.stripIndent()
}

def proc_git = "git -C $baseDir rev-parse HEAD".execute()
version = proc_git.text.trim()

params.help = false
if (params.help){
    println(params)
    helpMessage()
    exit 0
}

fastq_files = Channel.fromPath(params."fastq")
				   .map {it -> [it.simpleName, it]}



process flye {

    container 'liamtkane/pacasus'

    memory '30 G'
    
    cpus 8

    publishDir "pacasus/", mode: 'copy', overwrite: true, pattern: "*/*"

    input:
    set val(sample_id), file(fastq) from fastq_files

    output:
    file ("${sample_id}/*") into output

    script:
    sample_id = fastq.name.split('.')[0]
    """
    python3 pacasus.py ${fastq} -o ${params."out_file"} --loglevel=DEBUG
    """
}
