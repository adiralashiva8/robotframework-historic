pipeline {
    agent {label 'tommy_test'}
    stages {
                stage("Pull Repository")
                {
                    agent { label "tommy_test" }
                    steps {
                        script{container('qe-docker') {
                        git branch: 'master', url: 'git@github.com/Accruent/robotframework-historic.git'
                        }}
                    }
                }
            }
        }
