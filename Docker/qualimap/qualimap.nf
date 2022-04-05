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


process qualimap {

    container 'liamtkane/qualimap'

    input:
    set file(bam) from params."bam"

    script:
    """
    qualimap bamqc -bam ${bam} -outdir out/ -outformat HTML
    """
}
