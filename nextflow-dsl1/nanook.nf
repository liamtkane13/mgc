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


process nanook {

	container 'biocontainers/nanook:v1.33dfsg-1-deb_cv1'

}