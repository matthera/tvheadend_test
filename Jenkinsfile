pipeline {
	
	stages {
		stage('Checkout') {
			dir ('scm') {
				git 'https://github.com/tvheadend/tvheadend'
				def commit_tag = sh script: 'git rev-list -n 1 HEAD' returnStdout: true
				def version_tag = sh script: 'git describe' returnStdout: true
			}
			echo 'Build commit ${version_tag} : ${commit_tag}'
		}
	}
}
