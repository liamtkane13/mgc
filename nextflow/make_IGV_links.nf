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


params."git_dir" = '~/software'

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
    stdout into tmp_dir  

    script:
    """
    python3 ${git_dir}/liam_git/utils/IGV_s3_bucket.py
    """
}

process s3_sync {

    input:
    val(dir) from tmp_dir
    file(bam) from params."bam"
    file(ref) from params."ref"

    script:
    """
    aws s3 cp ${bam} s3://mgcdata/shared/igv-links/${dir}/
    aws s3 cp ${ref} s3://mgcdata/shared/igv-links/${dir}/
    s3cmd setacl s3://mgcdata/shared/igv-links/${dir}/${bam} --acl-public
    s3cmd setacl s3://mgcdata/shared/igv-links/${dir}/${ref} --acl-public
    """
}