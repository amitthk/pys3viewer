import java.text.SimpleDateFormat


node {
currentBuild.result = "SUCCESS"
  try{
   def pythonHome;
   def project_id;
   def artifact_id;
   def aws_s3_bucket_name;
   def aws_s3_bucket_region;
   def timeStamp;
   def baseDir;
   def deploy_env;
   def deploy_userid;
   
   stage('Initalize'){
   //Get these from parameters later
       pythonHome = tool 'python-3.6.4'
	   project_id = 'pys3viewer';
	   aws_s3_bucket_name = 'jvcdp-repo';
	   aws_s3_bucket_region = 'ap-southeast-1';
	   timeStamp = getTimeStamp();
       baseDir = pwd();
	   currentBranch = getCurrentBranch();
	   deploy_env=getTargetEnv(currentBranch);
	   deploy_userid='ec2-user';
//	   artifact_id = version();
   }

   
   stage('Checkout') { // for display purposes
      // Get latest code from a GitHub repository
      checkout scm;
   }

def build_scripts = load "${baseDir} /jenkins/build_scripts.groovy";
def deploy_scripts = load "${baseDir} /jenkins/deploy_scripts.groovy";
def utility_scripts = load "${baseDir} /jenkins/utility.groovy";

   stage('Get UI Dependencies'){
       build_scripts.get_ui_dependencies();
   }
   stage('Build UI'){
       build_scripts.build_ui();
   }

    stage('Publish to S3'){
        build_scripts.publish_ui_to_s3();
  
    }

   stage ("Install Application Dependencies") {
        sh '''
            source bin/activate
            pip install -r <relative path to requirements file>
            deactivate
           '''
    }

   
   stage('Code Analysis'){

       echo 'perform code analysis here!'
   }
   
   
       stage ("Collect Static files") {
        sh '''
            source bin/activate
            python <relative path to manage.py> collectstatic --noinput
            deactivate
           '''
    }

	stage ("Run Unit/Integration Tests") {
        def testsError = null
        try {
            sh '''
                source ../bin/activate
                python <relative path to manage.py> jenkins
                deactivate
               '''
        }
        catch(err) {
            testsError = err
            currentBuild.result = 'FAILURE'
        }
        finally {
            junit 'reports/junit.xml'

            if (testsError) {
                throw testsError
            }
        }
    }

  stage('Build'){
    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
    accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
    credentialsId: 's3mavenadmin', 
    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])  
	{
          awsIdentity() //show us what aws identity is being used
        def targetLocation = 'vendor_binaries/Python-3.6.3.tgz';
        withAWS(region: aws_s3_bucket_region) {
        s3Download(pathStyleAccessEnabled: true, file: 'Python-3.6.3.tgz', bucket: aws_s3_bucket_name, path: targetLocation);
		s3Download(pathStyleAccessEnabled: true, file: 'virtualenv-15.1.0.tar.gz', bucket: aws_s3_bucket_name, path: targetLocation);
        }
	}
	sh """
	   tar xzf Python-3.6.3.tgz
	   cd Python-3.6.3.tgz
	   mkdir -p ~/.localpython
	   ./configure --prefix=$HOME/.localpython
	   make
	   make install
	   mkdir -p src
	   tar -zxvf virtualenv-15.1.0.tar.gz ./src
	   cd virtualenv-15.1.0
	   ~/.localpython/bin/python setup.py install
	   python -m virtualenv ve -p $HOME/.localpython/bin/python3.6
	   source ve/bin/activate
	   
	
	"""
  }
   stage('Stash')
   {
      stash includes: 'dist/*.tar.gz', name: 'dist'
   }

/*    stage('Send Build to S3')
    {
    unstash 'dist';
    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
    accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
    credentialsId: 's3mavenadmin', 
    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])  
	 {
        awsIdentity() //show us what aws identity is being used
        def distLocation = project_id + '/builds/' + timeStamp;
        withAWS(region: aws_s3_bucket_region) {
        s3Upload(file: 'dist', bucket: aws_s3_bucket_name, path: distLocation)
        }
     }
    }
*/
	if(deploy_env=="all"){
	def envlist = ["dev", "sit", "uat", "staging","prod"];
		for(itm in envlist){
			stage("Checkpoint ${itm}"){
				checkAndDeploy(baseDir, itm, timeStamp, deploy_userid, project_id);
			}
		}
	}
	else{
		if(deploy_env!='none')
		{
			stage("Deploy to ${deploy_env}")
			{
				checkAndDeploy(baseDir, deploy_env, timeStamp, deploy_userid, project_id);
			}
		}
	}
  } catch (err) {

        currentBuild.result = "FAILURE"

        throw err
    }
}
