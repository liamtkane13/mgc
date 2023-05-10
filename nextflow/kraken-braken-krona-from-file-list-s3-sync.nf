#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:

       Mandatory arguments:
           --file              File with RSPs to run kraken on 
       Optional arguments:
           --out_dir        Output Directory (for things that aren't intermediate files to keep)
    """.stripIndent()
}

//defaults:
params."out_dir"        = 'out'
params."kraken2_db_dir" = '/NGS/Kraken-DB/k2_pluspfp_16gb_20220908/'
params."kmer_size"      = 100
params."plot_name"      = 'kraken2'
params."git_dir"   = '/home/ubuntu/software/liam_git'
params."kann_mongo_cred" = '/home/ubuntu/.kannapedia_mongo_credentials'
params."aws_source_cred" = '/home/ubuntu/.aws_batch'

def proc_git = "git -C $baseDir rev-parse HEAD".execute()
version = proc_git.text.trim()

params.help = false
if (params.help){
    println(params)
    helpMessage()
    exit 0
}



process read_rsp_file {
    publishDir params."out_dir" + '/' + 'rsps.txt', mode: 'copy', overwrite: true, pattern: 'rsps.txt'
    container 'medicinalgenomics/r-with-bam-vcf'
    memory '500 MB'
    cpus 1

    input:
    file(rsp_file) from file(params."rsp_file")
    //file(rsps_txt) from file('rsps.txt')

    output:
    stdout into rsps
    file('rsps.txt') into read_rsp_file

    """
    cat ${rsp_file}
    cp ${rsp_file} rsps.txt
    """
}

rsps
   .flatMap {n -> n.split(/\n/).collect()}
   .set{rsps}


process print_fastq_file_paths {

    container 'liamtkane/python_aws'

    input:
    val(rsp) from rsps 
    file(git_dir) from file(params."git_dir")
    file(kann_mongo_cred) from file(params."kann_mongo_cred")

    output:
    val(rsp) into rsp_out
    set val('*R1_001.fastq.gz'), val('*R2_001.fastq.gz') into fastq_file_paths

    script:
    """
    source ${kann_mongo_cred}
    python3 ${git_dir}/utils/query_mongo_return_fastqs.py -a ${rsp} | tr -d '\n'  
    """

} 

fastq_file_paths
    .map{it -> [it[0], it[1]]}
    .set {fastq_paths}

process pull_fastq_files {

   container 'liamtkane/python_aws'
   
   input:
   val(rsp) from rsp_out 
   set val(fq1), val(fq2) from fastq_paths
   file(aws_source_cred) from file(params."aws_source_cred")


   output:
   set val(rsp), file('*R1_001.fastq.gz'), file('*R2_001.fastq.gz') into fastq_files

   script:
   """
   source $aws_source_cred
   aws s3 cp ${fq1} .
   aws s3 cp ${fq2} .
   """
}

/*

kraken2_db_file_list = Channel.from(['/NGS/Kraken-DB/k2_pluspfp_16gb_20220908/'])


kraken2_db_file_list
	.map {it -> file(it)}
	.map {it -> [it, it.simpleName]}
	.set {kraken2_db}

kraken2_db.into {
    kraken2_db1
    kraken2_db2
}

kraken2_db2
    .view()



trim_galore_input_flat
	.combine(kraken2_db1)
	.set {kraken2_input}

kraken2_input.into {
    kraken2_input1
    kraken2_input2
}

process kraken2 {

    publishDir params."out_dir" + '/kraken-kreport/', mode: 'copy', overwrite: true, pattern: '*kreport2'

    tag {'kraken2' + '-' + id_run}

    container 'medicinalgenomics/kraken-braken-krona:latest'

    //should be able to do two at a time on using 8CPU/32G:
    memory '30 G'
    cpus 8

    input:
    set val(id_run), file(fq1), file(fq2), file(kraken2_db_dir), val(db_name) from kraken2_input1

    output:
    set val(id_run), val(db_name), file(kraken2_db_dir), file("*kreport2") into kraken2_output

    script:
    cpu    = task.cpus
    id_sample = id_run
    """
    /opt/kraken2/kraken2 \
    	--db ${kraken2_db_dir} \
    	--threads ${cpu} \
    	--report ${id_run}-${db_name}.kreport2 \
    	--paired ${fq1} ${fq2} \
    	> ${id_run}-${db_name}.kraken2

    #these files are big and we aren't doing anything with them, but they could be useful as they give per-read information.
    #probably best to add a --do_not_delete argument when needed:

    rm ${id_run}-${db_name}.kraken2
    rm ${fq1}
    rm ${fq2}
    """
}

/////// Krona for species ////////

process bracken_species {

	publishDir params."out_dir" + '/bracken-species/', mode: 'copy', overwrite: true, pattern: '*bracken_species*kreport2'

    tag {'bracken' + '-' + id_run}

    container 'medicinalgenomics/kraken-braken-krona:latest'

    memory '4 G'
    cpus 1

    input:
    set val(id_run), val(db_name), file(kraken2_db_dir), file(kreport2_input) from kraken2_output
    val(kmer_size) from params."kmer_size"

    output:
    set val(id_run), val(db_name), val(kmer_size), file("*bracken*.kreport2") into bracken_output_species

    script:
    cpu    = task.cpus
    id_sample = id_run
    """
    /opt/Bracken-2.8/bracken \
    	-d ${kraken2_db_dir} \
    	-i ${kreport2_input} \
    	-r ${kmer_size} \
    	-o ${id_sample}-${db_name}-${kmer_size}.S \
    	-l S \
    	-w ${id_sample}-${db_name}_bracken_species-${kmer_size}.kreport2
    """
}

process bracken_species_to_krona {
	publishDir params."out_dir" + '/kraken2-krona-species/', mode: 'copy', overwrite: true, pattern: '*.krona'

    tag {'bracken_species_to_krona' + '-' + id_run}

    container 'medicinalgenomics/kraken-braken-krona:latest'

    memory '4 G'
    cpus 1

    input:
    set val(id_run), val(db_name), val(kmer_size), file(bracken_kreport2) from bracken_output_species

    output:
    set val(id_run), val(db_name), val(kmer_size), file("*.krona") into bracken_species_to_krona_out

    script:
    cpu    = task.cpus
    id_sample = id_run
    """
    /opt/KrakenTools/kreport2krona.py \
    	-r ${bracken_kreport2} \
    	-o ${id_run}-${db_name}-${kmer_size}-species.krona
    """
}
*/