node {
currentBuild.result = "SUCCESS"
  try{
   def pythonHome;
   def project_id;
   def ui_project_id;
   def api_project_id;
   def artifact_id;
   def aws_s3_bucket_name;
   def aws_s3_bucket_region;
   def timeStamp;
   def baseDir;
   def deploy_env;
   def deploy_userid;
   def repo_bucket_credentials_id;
   def utility_scripts;
   def build_scripts;
   def deploy_scripts;

   
   stage('Checkout') {
      checkout scm;
   }
   stage('Initalize'){
       pythonHome = '/usr/local/bin/python3.6' ;
	   project_id = 'pys3viewer';
	   ui_project_id = 'pys3viewerui';
	   api_project_id = 'pys3viewerapi';
	   aws_s3_bucket_name = 'pys3viewer-repo';
	   aws_s3_bucket_region = 'ap-southeast-1';
       utility_scripts = load "jenkins/utility.groovy";
	   timeStamp = utility_scripts.getTimeStamp();
       baseDir = pwd();
	   currentBranch = utility_scripts.getCurrentBranch();
	   deploy_env = utility_scripts.getTargetEnv(currentBranch);
	   deploy_userid='ec2-user';
       repo_bucket_credentials_id = 's3repoadmin';
       build_scripts = load "jenkins/build_scripts.groovy";
       deploy_scripts = load "jenkins/deploy_scripts.groovy";
   }

	stage('UI Cleanup'){
		build_scripts.ui_cleanup(baseDir, ui_project_id, deploy_env, timeStamp);
	}

	stage('UI Dependencies'){
		build_scripts.ui_get_dependencies(baseDir, ui_project_id, deploy_env, timeStamp);
	}

	stage('UI Code Analysis'){
		build_scripts.ui_code_analysis(baseDir, ui_project_id, deploy_env, timeStamp);
	}

	stage('UI Build'){
		build_scripts.ui_build(baseDir, ui_project_id, deploy_env, timeStamp);
	}

	stage('UI Archive')
	{
		build_scripts.ui_archive(baseDir, ui_project_id, deploy_env, timeStamp);
	}

    stage('UI Publish')
	{
        def stash_dist_path = "${ui_project_id}/release/*.tar.gz";
		build_scripts.publish_to_s3(ui_project_id, stash_dist_path, aws_s3_bucket_region, aws_s3_bucket_name, repo_bucket_credentials_id, timeStamp);
	}

    stage('API Cleanup'){
		build_scripts.api_cleanup(baseDir, api_project_id, deploy_env, pythonHome, timeStamp);
	}
/*
	stage('API Dependencies'){
		build_scripts.api_get_dependencies(baseDir, api_project_id, deploy_env, pythonHome, timeStamp);
	}

	stage('API Code Analysis'){
		build_scripts.api_code_analysis(baseDir, api_project_id, deploy_env, pythonHome, timeStamp);
	}
*/
	stage('API Build'){
		build_scripts.api_build(baseDir, api_project_id, deploy_env, pythonHome, timeStamp);
	}

	stage('API Archive')
	{
		build_scripts.api_archive(baseDir, api_project_id, deploy_env, pythonHome, timeStamp);
	}

	stage('API Publish')
	{
        def stash_dist_path = "release/*.tar.gz";
		build_scripts.publish_to_s3(api_project_id, stash_dist_path, aws_s3_bucket_region, aws_s3_bucket_name, repo_bucket_credentials_id, timeStamp);
	}
/*
    if(deploy_env=="all"){
    def envlist = ["dev", "sit", "uat", "staging","prod"];
        for(itm in envlist){
            stage("Checkpoint ${itm}"){
                deploy_scripts.checkAndDeploy(baseDir, itm, timeStamp, deploy_userid, project_id);
            }
        }
    }
    else{
        if(deploy_env!='none')
        {
            stage("Deploy to ${deploy_env}")
            {
                deploy_scripts.checkAndDeploy(baseDir, deploy_env, timeStamp, deploy_userid, project_id);
            }
        }
    }
*/
  } catch (err) {

        currentBuild.result = "FAILURE"

        throw err
    }
}
