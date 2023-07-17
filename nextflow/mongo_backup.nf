#!/usr/bin/env nextflow

def helpMessage() {
    log.info"""
    ============================================================================
     :  Git version: ${version}
    ============================================================================
    Usage:
       Mandatory arguments:
           --f          Path to entrance file           
    """.stripIndent()
}

params."aws_source_cred" = '/home/ubuntu/.aws_batch'

def proc_git = "git -C $baseDir rev-parse HEAD".execute()
version = proc_git.text.trim()

params.help = false
if (params.help){
    println(params)
    helpMessage()
    exit 0
}

process get_date {

	output:
	stdout into date_output

	script:
	"""
	backup_date="\$(date +'%Y%m%d')"

	echo \${backup_date} | tr -d '\n'
	"""	
}

process perform_backup {

	input:
	file(pw_file) from file(params."f")
	val(backup_date) from date_output

	output:
	set val(backup_date), file("${backup_date}") into backup_output

	script:
	"""
	cat ${pw_file} | mongodump --host 75.101.255.79:27017 --out ${backup_date} --db mgc_ss2_JL --username liam	
	""" 
}


process s3_sync {

	container 'liamtkane/python_aws'

	input:
	set val(date), file(backup_dir) from backup_output
//	file(aws_source_cred) from file(params."aws_source_cred")	

	script:
	/*"""
	 source $aws_source_cred */
	""" 
	aws s3 sync ${backup_dir} s3://mgcdata/backup/mongodb/bson/${date}/
	""" 
}