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
           --run_name              Batch/run name for output tsv
           --s3_path               s3 path for BAM files, used in constructing IGV links (e.g. 'rnaseq-2023-hlvd/march22_2023_RNASeq/virus_mapping/out/bam/')
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
    echo -e 'Accession\tVirus_Length\t${sample_id}_Mapped_Bases\t${sample_id}_Mean_Coverage\t${sample_id}_Standard_Deviation' > ${sample_id}-cov-per-virus.tsv
    
	cat ${dir}/${sample_id}/${sample_id}/genome_results.txt | grep 'gi|' | sed -e 's/^[ \t]*//' | cut -f 2 -d 'f' | sed -e 's/|//'| sed -e 's/|//' >> ${sample_id}-cov-per-virus.tsv
	"""
}


parse_qualimap_output
    .map{it -> [it[1]]}
    .collect()
    .view()
    .set{write_tsv_input}


process write_tsv {

    publishDir "${params.out_dir}" +'/', mode: 'copy', overwrite: false, pattern: "*"

    input:
    file(sample_tsv) from write_tsv_input
    val(batch) from params."run_name"
    val(s3_path) from params."s3_path"

    output:
    file("*.tsv") into write_tsv_output
    script:
    """
    python3 /Users/liamkane/software/liam_git/utils/parse_qualimap_cov_tsv.py --i ${sample_tsv} --b ${batch} --p ${s3_path}
    """
}     
