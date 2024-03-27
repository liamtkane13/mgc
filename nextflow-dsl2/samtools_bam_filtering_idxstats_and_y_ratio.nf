#!/usr/bin/env nextflow 

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
       Mandatory arguments:
           --bam			   BAM files to filter   
        Optional arguments:
           --git_dir           Github Directory (e.g. '~/software/mgc/')  
           --variable_flag     Do you want to test variable flags?
           --flag_file         File of samtools flags to test            
    """.stripIndent()
}

params."out_dir" = 'out'
params."git_dir" = '/home/ubuntu/liam/liam_git'
params."variable_flag" = 'false'
params."flag_file" = 'NULL'

def proc_git = "git -C $baseDir rev-parse HEAD".execute()
version = proc_git.text.trim()

params.help = false
if (params.help){
    println(params)
    helpMessage()
    exit 0
}


process read_flag_file {     

    input:
    file(flag_file) 
    val(variable_flag) 

    output:
    stdout 

    """
    if (${variable_flag} == 'true')
    then
        cat ${flag_file}
    else
        echo "No Flags"
    fi    
    """
}


process filter_bam_files {

    publishDir params."out_dir", mode: 'copy', overwrite: true, pattern: '*-idxstats.tsv'

    cpus 4 

	input:
	tuple val(rsp), file(bam), val(flag)
//    val(flag) 
    val(variable_flag) 

	output:
	file("*-idxstats.tsv") 

	script:
    cpu    = task.cpus
	"""
    if (${variable_flag} == 'true')
    then 
        samtools view -F ${flag} --bam ${bam} --threads $cpu | samtools idxstats - >>  ${rsp}-${flag}-idxstats.tsv
        samtools view --bam ${bam} --threads $cpu | samtools idxstats - >>  ${rsp}-idxstats.tsv
    else
        samtools view --bam ${bam} --threads $cpu | samtools idxstats - >>  ${rsp}-idxstats.tsv   
    fi    
    """
}


process calculate_y_ratio {

    publishDir params."out_dir", mode: 'copy', overwrite: true, pattern: 'y-ratios.txt'

    input:
    file(idxstats) 
    file(git_dir) 

    output:
    tuple file("y-ratios.txt"), file(git_dir)

    script:
    """
    python3 ${git_dir}/utils/calculate_y_ratio_from_idxstats_output.py -i ${idxstats} >> y-ratios.txt    
    """
}


process plot_y_ratios {

    publishDir params."out_dir", mode: 'copy', overwrite: true, pattern: 'y_ratio_plot.png'

    input:
    tuple file(y_ratios), file(git_dir)

    output:
    file("y_ratio_plot.png")

    script:
    """
    python3 ${git_dir}/utils/plot_y_ratio.py -i ${y_ratios}
    """
}



workflow {

    flag_file = channel.fromPath(params."flag_file")

    flag_list = read_flag_file(flag_file, params."variable_flag")

    flag_list
        .flatMap {n -> n.split(/\n/).collect()}
        .set{flags} 

    bam_files = Channel.fromPath(params."bam")
                                    .map {it -> [it.simpleName, it]}
                                    .combine(flags)
                                    .view()      

    filter_bam_files_output = filter_bam_files(bam_files, params."variable_flag")

    filter_bam_files_output
        .collect()
        .view()
        .set {filter_bam_files_output_1}

    calculate_y_ratio_output = calculate_y_ratio(filter_bam_files_output_1, file(params."git_dir"))

    y_ratio_plot = plot_y_ratios(calculate_y_ratio_output) 
}