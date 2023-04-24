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
           --bed                   Path to BED file, if wanted  
           --git_dir               Github Directory (e.g. '~/software/mgc/') 
    """.stripIndent()
}


params."git_dir" = '/home/ubuntu/software'
params."aws_source_cred" = '/home/ubuntu/.aws_batch'

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
    file(ref) from file(params."ref")
    file(aws_source_cred) from file(params."aws_source_cred")

    script:
    """
    source $aws_source_cred 
    aws s3 cp ${bam} s3://mgcdata/shared/igv-links/tmp/${dir}/
    aws s3 cp ${ref} s3://mgcdata/shared/igv-links/tmp/${dir}/
    s3cmd setacl s3://mgcdata/shared/igv-links/tmp/${dir}/${bam} --acl-public
    s3cmd setacl s3://mgcdata/shared/igv-links/tmp/${dir}/${ref} --acl-public
    """
}