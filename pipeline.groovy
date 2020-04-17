pipeline {
    agent {label 'tommy_test'}
    stages {
                stage("Pull Repository") {
                    steps {
                        script{container('qe-docker') {
                        git branch: 'master', url: 'https://github.com/Accruent/robotframework-historic.git'
                        }}
                    }
                }
	    
		stage('Build image') {
                    	steps {
				script{container('qe-docker') {
				sh 'sleep 2000'	
				def app	
				app = docker.build("proget.accruentsystems.com/qe_docker/rfhistoric")
				}}
			}
		}

		stage('Push image') {
                    	steps {
				script{container('qe-docker') {
				docker.withRegistry('http://proget.accruentsystems.com/qe_docker/', 'svcselenium') {
				app.push("${env.BUILD_NUMBER}")
				app.push("latest")
			}}	
            }
        }
	}
	}
	}
