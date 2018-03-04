def check_install_virtualenv(){
    def installed = fileExists 'bin/activate'
    if (!installed) {
        stage("Install Python Virtual Enviroment") {
            sh "${pythonHome} -m virtualenv --no-site-packages ."
        }
    }   
}

def get_ui_dependencies(){
    		sh '''
		    cd pys3viewerui
		    rm -rf dist
		    rm -rf dist.tar.gz
		    rm -rf rm -rf release/*.tar.gz
		    npm install
		    '''
}

def build_ui(){
    		sh '''
		    cd pys3viewerui
		    npm run ng build --prod -- --environment=${deploy_env} --max-old-space-size=200
		    '''
}

def archive_and_stash_ui(){
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

def publish_ui_to_s3(String project_id, String aws_s3_bucket_region, String aws_s3_bucket_name, String aws_credentials_id, String timeStamp){
	withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-deployuser', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])
	{
		unstash 's3mavenadmin'
		awsIdentity() //show us what aws identity is being used
		def targetLocation = project_id + '/' + timeStamp;
		withAWS(region: aws_s3_bucket_region) {
		s3Upload(file: 'release', bucket: aws_s3_bucket_name, path: targetLocation)
		}
	}
}

def performUIBuild(String timeStamp, String project_id,String deploy_env, String npmHome){

	stage('Clean'){
		sh 'rm -rf dist && rm -rf dist.tar.gz && rm -rf release/*.tar.gz'
	}

	stage('Get Dependencies'){
		withEnv(["PATH+NODE=${npmHome}/bin","NODE_HOME=${npmHome}"]) {
			sh "npm install --max-old-space-size=200"
		}
	}

	stage('Code Analysis'){
		try{
			withEnv(["PATH+NODE=${npmHome}/bin","NODE_HOME=${npmHome}"]) {
				sh '$npm run lint'
			}
		}catch(err){
			echo 'Code Quality Analysis failed!'
		}
	}

	stage('Build'){
		withEnv(["PATH+NODE=${npmHome}/bin","NODE_HOME=${npmHome}"]) {
			sh "npm run build -- --prod --environment=${deploy_env} --max-old-space-size=200"
		}
	}

	stage('Archive')
	{
		sh 'mkdir -p release'
		sh "cd dist && tar -czvf ../release/${project_id}-${timeStamp}.tar.gz . && cd .."
		stash includes: 'release/*.tar.gz', name: "${project_id}"
		stash includes: 'dist/**/*', name: "${project_id}_dist"
	}
}

return this;