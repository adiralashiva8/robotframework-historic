pipeline {
    agent {label 'tommy_test'}
    stages {
                stage("Pull Repository")
                {
                    agent { label "tommy_test" }
                    steps {
                        script{container('qe-docker') {
                        git branch: 'master', url: 'https://github.com/Accruent/robotframework-historic.git'
                        }}
                    }
                }
				    stage('Build image') {
					app = docker.build("proget.accruentsystems.com/qe_docker/rfhistoric")
					}

					stage('Push image') {
						docker.withRegistry('http://proget.accruentsystems.com/qe_docker/', 'svcselenium') {
						app.push("${env.BUILD_NUMBER}")
						app.push("latest")
					}
					echo "Trying to Push Docker Build to Proget"
					}	
            }
        }
