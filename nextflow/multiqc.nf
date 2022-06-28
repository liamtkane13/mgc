#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
       Mandatory arguments:
           --in_dir         Input Directory containing QC files
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

///input_directory = Channel.fromPath(params."in_dir")
///				   .map {it -> [it.simpleName, it]}

input_dir = Channel.fromPath(params."in_dir", type: 'dir')

process multiqc {

    container 'medicinalgenomics/multiqc'

    publishDir "multiqc_output/", mode: 'copy', overwrite: true, pattern: "*/*"

    input:
    path(qc_file) from input_dir

    output:
    file ("${sample_id}_multiqc/*") into output

    script:
    sample_id = qc_file.name.split('/')[0]
    """
    multiqc -o ${sample_id}_multiqc/ $qc_file/
    """
}
