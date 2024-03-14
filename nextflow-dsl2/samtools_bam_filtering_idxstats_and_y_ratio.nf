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
params."flag_file" = ''

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
    file(flag_file) from file(params."flag_file")
    val(variable_flag) from params."variable_flag"

    output:
    stdout into flag_list

    """
    if (${variable_flag} == 'true')
    then
        cat ${flag_file}
    else
        echo "No Flags"
    fi    
    """
}

flag_list
    .flatMap {n -> n.split(/\n/).collect()}
//  .toList()
    .set {flags}

flags.into {

    flags_1
    flags_2
}

flags_2
    .view()



bam_files = Channel.fromPath(params."bam")
                                    .map {it -> [it.simpleName, it]}    

bam_files
    .join {flags_1}
    .view()

/*
process filter_bam_files {

    publishDir params."out_dir", mode: 'copy', overwrite: true, pattern: '*-idxstats.tsv'

    cpus 4 

	input:
	set val(rsp), file(bam) from bam_files
    val(flag) from flags_1
    val(variable_flag) from params."variable_flag" 

	output:
	file("*-idxstats.tsv") into filter_bam_files_output

	script:
    cpu    = task.cpus
	"""
    if (${variable_flag} == 'true')
    then 
        flag_num="\$(echo ${flag} | cut -f 2 -d ' ')"
        samtools view ${flag} --bam ${bam} --threads $cpu | samtools idxstats - >>  ${rsp}-"\${flag_num}"-idxstats.tsv
    else
        samtools view --bam ${bam} --threads $cpu | samtools idxstats - >>  ${rsp}-idxstats.tsv   
    fi    
    """
}

filter_bam_files_output
    .collect()
    .view()
    .set {filter_bam_files_output_1}



process calculate_y_ratio {

    publishDir params."out_dir", mode: 'copy', overwrite: true, pattern: 'y-ratios.txt'

    input:
    file(idxstats) from filter_bam_files_output_1
    file(git_dir) from file(params."git_dir")

    output:
    file("y-ratios.txt") into calculate_y_ratio_output

    script:
    """
    python3 ${git_dir}/utils/calculate_y_ratio_from_idxstats_output.py -i ${idxstats} >> y-ratios.txt    
    """
}



process plot_y_ratios {

    publishDir params."out_dir", mode: 'copy', overwrite: true, pattern: 'y_ratio_plot.png'

    input:
    file(y_ratios) from calculate_y_ratio_output
    file(git_dir) from file(params."git_dir")

    output:
    file("y_ratio_plot.png") into plot_y_ratios_output

    script:
    """
    python3 ${git_dir}/utils/plot_y_ratio.py -i ${y_ratios}
    """
} */