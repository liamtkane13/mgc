def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
        Mandatory arguments:
           --ref                   Path to reference FASTA 
           --bam                   Path to BAM Files 
           --out_dir          	   Output Directory (for things that aren't intermediate files to keep)
        Optional arguments:
           --locus                 Locus to focus on for IGV  
           --git_dir               Github Directory (e.g. '~/software/mgc/') 
    """.stripIndent()
}


params."git_dir" = '/home/ubuntu/software'
params."aws_source_cred" = '/home/ubuntu/.aws_batch'
params."out_dir" = 'out/'
params."locus" = 'false'

def proc_git = "git -C $baseDir rev-parse HEAD".execute()
version = proc_git.text.trim()

params.help = false
if (params.help){
    println(params)
    helpMessage()
    exit 0
}


process make_tmp_dir {

    container 'liamtkane/python_aws'

    input:
    file(git_dir) from file(params."git_dir") 

    output:
    stdout into tmp_dir_ex 

    script:
    """
    python3 ${git_dir}/liam_git/utils/IGV_s3_bucket.py
    """
}

tmp_dir_ex
    .trim()
    .set {tmp_dir}

process s3_sync {

    container 'liamtkane/python_aws'

    input:
    val(dir) from tmp_dir
    file(bam) from file(params."bam")
    file(bai) from file(params."bam" + '.bai')
    file(ref) from file(params."ref")
    file(index) from file(params."ref" + '.fai')
    file(aws_source_cred) from file(params."aws_source_cred")

    output:
    val(dir) into s3_sync_output

    script:
    """
    source $aws_source_cred 
    aws s3 cp ${bam} s3://mgcdata/shared/igv-links/tmp/${dir}/
    aws s3 cp ${bai} s3://mgcdata/shared/igv-links/tmp/${dir}/
    aws s3 cp ${ref} s3://mgcdata/shared/igv-links/tmp/${dir}/
    aws s3 cp ${index} s3://mgcdata/shared/igv-links/tmp/${dir}/
    s3cmd setacl s3://mgcdata/shared/igv-links/tmp/${dir}/${bam} --acl-public
    s3cmd setacl s3://mgcdata/shared/igv-links/tmp/${dir}/${bai} --acl-public
    s3cmd setacl s3://mgcdata/shared/igv-links/tmp/${dir}/${ref} --acl-public
    s3cmd setacl s3://mgcdata/shared/igv-links/tmp/${dir}/${index} --acl-public
    """
}

locus_test = Channel.from(params."locus")

locus_test.into{
    locus_1
    locus_2
}

locus_1
    .view()

process write_link {

    publishDir "${params.out_dir}" +'/', mode: 'copy', overwrite: true, pattern: "*"

    container 'liamtkane/python_aws'

    input:
    val(dir) from s3_sync_output
    file(git_dir) from file(params."git_dir")
    file(aws_source_cred) from file(params."aws_source_cred")
    val(locus) from locus_2

    output:
    file('*.txt') into write_link_output

    script:
    """
    if (${locus} == 'false') 
    then
        source $aws_source_cred
        python3 ${git_dir}/liam_git/utils/write_IGV_links.py -b ${dir}
    else
        source $aws_source_cred
        python3 ${git_dir}/liam_git/utils/write_IGV_links_with_locus.py -b ${dir} -l ${locus}
    fi    
    """
}