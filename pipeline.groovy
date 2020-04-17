pipeline {
    agent {label 'tommy_test'}
    stages {
                stage("Pull Repository")
                {
                    agent { label "tommy_test" }
                    steps {
                        script{container('qe-docker') {
                        git branch: 'master', url: 'github.com/Accruent/robotframework-historic.git'
                        }}
                    }
                }
            }
        }
