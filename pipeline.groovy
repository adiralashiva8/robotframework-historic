node {
    def app

    stage('Clone repository') {
        /* Cloning the Repository to our Workspace */

        checkout scm
    }

    stage('Build image') {
        /* This builds the actual image */

        app = docker.build("proget.accruentsystems.com/qe_docker/rfhistoric")
    }
/*
    stage('Test image') {

        app.inside {
            echo "Tests passed"
        }
    }
*/
    stage('Push image') {
        /*
			You would need to first register with DockerHub before you can push images to your account
		*/
        docker.withRegistry('proget.accruentsystems.com', 'svcselenium') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
            }
                echo "Trying to Push Docker Build to DockerHub"
    }
}
