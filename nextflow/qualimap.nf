#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
       Mandatory arguments:
           --bam            BAM file for QC
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

    input:
    set val(sample_id), file(bam) from bam_files

    script:
    """
    qualimap bamqc -bam ${bam} -outdir ${sample_id}/ -outformat HTML
    """
}
