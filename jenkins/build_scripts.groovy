def ui_cleanup(String baseDir, String project_id,String deploy_env,  String timeStamp){
	sh "cd ${baseDir}/${project_id} && rm -rf dist && rm -rf dist.tar.gz && rm -rf release/*.tar.gz"
}

def ui_get_dependencies(String baseDir, String project_id,String deploy_env,  String timeStamp){
	withNPM(npmrcConfig: '.npmrc'){
		sh "cd ${baseDir}/${project_id} && npm install --max-old-space-size=200"
	}
}

def ui_code_analysis(String baseDir, String project_id,String deploy_env,  String timeStamp){
	try{
		withNPM(npmrcConfig: '.npmrc'){
			sh 'cd ${baseDir}/${project_id} && npm run lint';
		}
	}catch(err){
		echo 'Code Quality Analysis failed!';
	}
}

def ui_build(String baseDir, String project_id,String deploy_env,  String timeStamp){
	withNPM(npmrcConfig: '.npmrc') {
		sh "cd ${baseDir}/${project_id} && npm run ng build --prod -- --environment=${deploy_env} --max-old-space-size=200"
	}
}

def ui_archive(String baseDir, String project_id,String deploy_env,  String timeStamp){
	sh "cd ${baseDir}/${project_id}/dist && tar -czvf ${baseDir}/${project_id}/dist/${project_id}-${timeStamp}.tar.gz ."
	stash includes: '${baseDir}/${project_id}/dist/*.tar.gz', name: "${project_id}_dist"
}

def api_cleanup(String baseDir, String project_id,String deploy_env, String pythonHome, String timeStamp){
	sh "cd ${baseDir} && rm -rf dist && rm -rf build"
}

def api_get_dependencies(String baseDir, String project_id,String deploy_env, String pythonHome, String timeStamp){
	withEnv(["PYTHON_HOME=${pythonHome}"]) {
		sh "cd ${baseDir}/${project_id} && npm install --max-old-space-size=200"
	}
}

def api_code_analysis(String baseDir, String project_id,String deploy_env, String pythonHome, String timeStamp){
	try{
		withEnv(["PYTHON_HOME=${pythonHome}"]) {
			sh 'cd ${baseDir}/${project_id} && pylint pys3viewer'
		}
	}catch(err){
		echo 'Code Quality Analysis failed!'
	}
}

def api_build(String baseDir, String project_id,String deploy_env, String pythonHome, String timeStamp){
	withEnv(["PYTHON_HOME=${pythonHome}"]) {
		sh "cd ${baseDir}/${project_id} && python install.py build"
	}
}

def api_archive(String baseDir, String project_id,String deploy_env, String pythonHome, String timeStamp){
	sh "cd ${baseDir}/${project_id}/build && tar -czvf ${baseDir}/${project_id}/build/${project_id}-${timeStamp}.tar.gz ."
	stash includes: '${baseDir}/${project_id}/build/*.tar.gz', name: "${project_id}_dist"
}


def api_setup_environment(){
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
	""";
}

def publish_to_s3(String project_id, String aws_s3_bucket_region, String aws_s3_bucket_name, String jenkins_credentials_id, String timeStamp){
	withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
	accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
	credentialsId: "${jenkins_credentials_id}", 
	secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])
	{
		unstash "${project_id}_dist"
		awsIdentity() //show us what aws identity is being used
		def distLocation = project_id + '/releases/';
		withAWS(region: aws_s3_bucket_region){
		s3Upload(file: 'dist', bucket: aws_s3_bucket_name, path: distLocation)
		}
	}
}


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
		    ''';
}

def build_ui(){
    		sh '''
		    cd pys3viewerui
		    npm run ng build --prod -- --environment=${deploy_env} --max-old-space-size=200
		    ''';
}

def archive_and_stash_ui(){
	sh '''
       cd pys3viewerui
       mkdir -p release
       cd dist
       tar -czvf ../release/${project_id}ui-${timeStamp}.tar.gz .
       cd ..
       ''';
       stash includes: 'release/*.tar.gz', name: "${project_id}_ui";
       stash includes: 'dist/**/*', name: "${project_id}_ui_dist";
}

return this;