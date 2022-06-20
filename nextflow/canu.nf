#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
       Mandatory arguments:
           --fastq          FASTQ files to be Assembled
           --size           Size of Genome being Assembled
           --prefix         Prefix to use for Output Files
           --out_dir        Output Directory (for things that aren't intermediate files to keep)
       Optional arguments:
           --run_dir        Directory for Canu to run in 
           
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



process canu {

    container 'greatfireball/canu'

    memory '30 G'
    
    cpus 8

    publishDir "${params."out_dir"}/canu/", mode: 'copy', overwrite: true, pattern: "*/*"

    input:
    set val(sample_id), file(fastq) from fastq_files

    output:
    file ("${sample_id}/*") into output

    script:
    sample_id = fastq.name.split('/')[0]
    """
    canu -p ${params."prefix"} genomeSize= ${params."size"} m -nanopore ${fastq}
    """
}
