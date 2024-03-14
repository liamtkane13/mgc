#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
       Mandatory arguments:
           --fasta          FASTA file for QC
           --out_dir        Output Directory (for things that aren't intermediate files to keep)
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

fasta_files = Channel.fromPath(params."fasta")
				   .map {it -> [it.simpleName, it]}


process quast {

    container 'liamtkane/quast'

    publishDir "${params.out_dir}/quast/", mode: 'copy', overwrite: true, pattern: "*/*"

    input:
    set val(sample_id), file(fasta) from fasta_files

    output:
    file ("${sample_id}/*") into output

    script:
    """
    quast.py -s -o $sample_id ${fasta}
    """
}
