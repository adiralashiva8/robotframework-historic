pipeline {
    agent {label 'tommy_docker'}
    stages {
                stage("Pull Repository")
                {
                    agent { label "tommy_docker" }
                    steps {
                        script{container('qe-docker') {
                        git branch: 'master', url: 'git@ithub.com/Accruent/robotframework-historic.git'
                        }}
                    }
                }
            }
        }
