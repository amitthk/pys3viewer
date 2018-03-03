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
   
   def installed = fileExists 'bin/activate'

    if (!installed) {
        stage("Install Python Virtual Enviroment") {
            sh 'virtualenv --no-site-packages .'
        }
    }   

   
   stage('Checkout') { // for display purposes
      // Get latest code from a GitHub repository
      checkout scm;
   }

   stage('Get UI Dependencies'){
		sh '''
		    cd pys3viewerui
		    rm -rf dist
		    rm -rf dist.tar.gz
		    rm -rf rm -rf release/*.tar.gz
		    npm install
		    '''
   }
   stage('Build UI'){
		sh '''
		    cd pys3viewerui
		    npm run ng build --prod -- --environment=${deploy_env} --max-old-space-size=200
		    '''
   }
   stage('Archive') {
       sh '''
       cd pys3viewerui
       mkdir -p release
       cd dist
       tar -czvf ../release/${project_id}ui-${timeStamp}.tar.gz .
       cd ..
       '''
       stash includes: 'release/*.tar.gz', name: "${project_id}_ui"
       stash includes: 'dist/**/*', name: "${project_id}_ui_dist"
   }
	withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-deployuser', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])
	 {
		stage('Publish to S3'){
		unstash 's3mavenadmin'
		awsIdentity() //show us what aws identity is being used
		def targetLocation = project_id + '/' + timeStamp;
		withAWS(region: aws_s3_bucket_region) {
		s3Upload(file: 'release', bucket: aws_s3_bucket_name, path: targetLocation)
		}
		}
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

def getTimeStamp(){
	def dateFormat = new SimpleDateFormat("yyyyMMddHHmm")
	def date = new Date()
	return dateFormat.format(date);
}

def getTargetEnv(String branchName){
	def deploy_env="dev";
	switch(branchName){
		case('develop'):
		deploy_env="dev";
		break;
		case('sit'):
		deploy_env="sit";
		break;
		case('uat'):
		deploy_env="uat";
		break;
		case('staging'):
		deploy_env="staging";
		break;
		case('master'):
		deploy_env="prod";
		break;
		case('cdp'):
		deploy_env="all";
		break;
		default:
			if(branchName.startsWith("feature")){
				deploy_env="none"
			}
		break;
	}
	return deploy_env;
}

def checkAndDeploy(String baseDir, String envname, String timeStamp,  String deploy_userid, String project_id){
	  def  c_userInput = false;
	  def c_didTimeout = false;

	if(envname=="dev"){
	//Deploy directly to dev environment
		run_playbook("main.yaml",envname,  deploy_userid, project_id);
	}
	else{

	try {
	    timeout(time: 5, unit: 'DAYS') { // change to a convenient timeout for you
	        c_userInput = input(message: "Do you approve deployment to ${envname}?", ok: "Proceed", 
                        parameters: [booleanParam(defaultValue: true, 
                        description: "If you would want to proceed for deployment to ${envname}, just tick the checkbox and click Proceed!",name: "Yes?")])
	    }
	} catch(err) { // timeout reached or input false
	    def user = err.getCauses()[0].getUser()
	    if('SYSTEM' == user.toString()) { // SYSTEM means timeout.
	        c_didTimeout = true
	    } else {
	        c_userInput = false
	        echo "Aborted by: [${user}]"
	    }
	}
        if ((c_didTimeout)||(!c_userInput)) {
            // do something on timeout
            echo "no input was received before timeout"
            currentBuild.result = 'ABORTED'
        } else {
			run_playbook("main.yaml",envname, deploy_userid, project_id);
        } 
   }
}

def run_playbook(playbook_name, deploy_env, String deploy_userid, String project_id) {
		
		def package_base_dir =  (pwd()+"/target/").toString();
		def extras_params = "-v -e deploy_host=${deploy_env} -e remote_user=${deploy_userid} -e package_base_dir=${package_base_dir}".toString();
		def playbook_to_run = ("ansible/" + playbook_name).toString();
		withEnv(['ANSIBLE_HOST_KEY_CHECKING=False']){
		ansiblePlaybook( 
		credentialsId: 'deployadmin',
        playbook: playbook_to_run,
        inventory: 'hosts', 
        extras: extras_params)
		}
}



def runWithServer(body) {
    def id = UUID.randomUUID().toString()
    deploy id
    try {
        body.call "${jettyUrl}${id}/"
    } finally {
        undeploy id
    }
}

def getCurrentBranch () {
    return sh (
        script: 'git rev-parse --abbrev-ref HEAD',
        returnStdout: true
    ).trim()
}
