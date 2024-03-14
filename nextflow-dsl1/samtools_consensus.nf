#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
       Mandatory arguments:
           --bam          BAM file to process
           --r            Region to query         
           --out_dir        
    """.stripIndent()
}

params."aws_source_cred" = '/home/ubuntu/.aws_batch'
params."git_dir" = '/home/ubuntu/software/mgc/'

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

process samtools_consensus {

    publishDir "${params.out_dir}" + "/", mode: 'copy', overwrite: true, pattern: "*/*"

    container 'medicinalgenomics/samtools-consensus'

    input:
    set val(sample_id), file(bam) from bam_files
    file(bai) from file(params."bam" + '.bai')
    val(region) from params."r"

    output:
    set val(sample_id), val(region), file("${sample_id}_HLVd.fasta") into samtools_consensus_output

    script:
    """
    samtools consensus ${bam} -r ${region} -a --ambig --show-del yes --show-ins yes > ${sample_id}_HLVd.fasta
    """ 
}