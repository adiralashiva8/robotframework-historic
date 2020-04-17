pipeline {
    def app
    agent {label 'tommy_docker'}
    
      stage('Clone repository') {
        checkout scm
      }
      
      stage('Build image') {
              app = docker.build("proget.accruentsystems.com/qe_docker/rfhistoric")
          }
          
          stage('Push image') {
              docker.withRegistry('http://proget.accruentsystems.com/qe_docker/', 'svcselenium') {
                  app.push("${env.BUILD_NUMBER}")
                  app.push("latest")
                  }
                      echo "Push Docker Build to Proget"
          }
}
