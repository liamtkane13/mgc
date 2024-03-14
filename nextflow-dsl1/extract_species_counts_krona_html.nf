#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
        Mandatory arguments:
           --krona_files           Path to Krona HTML Files for analysis
           --outfile_name          Name for output TSV
           --out_dir          	   Output Directory (for things that aren't intermediate files to keep)
    """.stripIndent()
}

params."git_dir" = '/home/ubuntu/software/liam_git/mgc' 

process process_and_write_tsv {

    publishDir "${params.out_dir}" +'/', mode: 'copy', overwrite: false, pattern: "*"

    container 'liamtkane/python_pandas' 

    input:
    file(sample_html) from params."krona_files"
    val(outfile) from params."outfile_name"
    file(git_dir) from params."git_dir"

    output:
    file("*.tsv") into write_tsv_output
    script:
    """
    python3 ${git_dir}/utils/parse_qualimap_cov_tsv.py --i ${sample_tsv} --b ${batch} --p ${s3_path}
    """
}