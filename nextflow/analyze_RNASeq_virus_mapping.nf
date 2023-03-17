#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
        Mandatory arguments:
           --sample_file           File of Sample Names (one per line) to process
           --qualimap_path         Path to QualiMap Output Directories for analysis
           --out_dir          	   Output Directory (for things that aren't intermediate files to keep)
    """.stripIndent()
}



process read_sample_file {
    publishDir params."out_dir" + '/' + 'rsps.txt', mode: 'copy', overwrite: true, pattern: 'rsps.txt'
    container 'medicinalgenomics/r-with-bam-vcf'
    memory '500 MB'
    cpus 1

    input:
    file(sample_file) from file(params."sample_file")

    output:
    stdout into samples
    file('samples.txt') into read_sample_file

    """
    cat ${sample_file}
    cp ${sample_file} samples.txt
    """
}

samples
   .flatMap {n -> n.split(/\n/).collect()}
   .set{samples}

samples.into {
    samples1
    samples2
    samples3
}


process parse_qualimap {

	publishDir "${params.out_dir}" +'/', mode: 'copy', overwrite: false, pattern: "*"

	input:
	val(sample_id) from samples1
    file(dir) from file(params."qualimap_path")

	output:
	set val(sample_id), file("${sample_id}-cov-per-virus.tsv") into parse_qualimap_output

	script:
	"""
	cat ${dir}/${sample_id}/${sample_id}/genome_results.txt | grep 'gi|' | sed -e 's/^[ \t]*//' > ${sample_id}-cov-per-virus.tsv
	"""
}	




