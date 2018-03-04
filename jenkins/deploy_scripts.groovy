
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

return this;