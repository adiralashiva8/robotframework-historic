pipeline {
    agent {label 'tommy_test'}
    stages {
                stage("Pull Repository") {
                    agent { label "tommy_test" }
                    steps {
                        script{container('qe-docker') {
                        git branch: 'master', url: 'https://github.com/Accruent/robotframework-historic.git'
                        }}
                    }
                }
	    
		stage('Build image') {
			agent { label "tommy_test" }
                    	steps {
				script{container('qe-docker') {
				def app	
				app = docker.build("proget.accruentsystems.com/qe_docker/rfhistoric")
				}}
			}
		}

		stage('Push image') {
			agent { label "tommy_test" }
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
