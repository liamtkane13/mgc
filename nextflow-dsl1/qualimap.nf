#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
       Mandatory arguments:
           --bam            BAM file for QC
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

bam_files = Channel.fromPath(params."bam")
				   .map {it -> [it.simpleName, it]}


process qualimap {

    container 'liamtkane/qualimap'

    publishDir "${params.out_dir}/qualimap/${sample_id}", mode: 'copy', overwrite: true, pattern: "*/*"

    input:
    set val(sample_id), file(bam) from bam_files

    output:
    file ("${sample_id}/*") into output

    script:
    """
    qualimap bamqc -bam ${bam} -outdir $sample_id -outformat HTML
    """
}
