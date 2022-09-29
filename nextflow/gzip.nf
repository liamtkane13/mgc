#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
       Mandatory arguments:
           --infile          Input file to be zipped
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

infiles = Channel.fromPath(params."infile")
                            .map {it -> [it.simpleName, it]}


process gzip {
    
    publishDir "${params.out_dir}/", mode: 'copy', overwrite: true, pattern: "*\*"
    memory '2 G'
    cpus 1

    input:
    set val(sample_id), file(infile) from infiles

    output:
    file("*") into output

    script:
    cpu = task.cpus
    memory = task.memor.toGiga()
    """
    gzip $infile
    """
}

