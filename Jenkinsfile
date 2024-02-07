pipeline {
    agent any

    options{
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment{
        registry = 'datdt185/text_summarization'
        registryCredential = 'dockerhub-credential'      
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building image for deployment..'
                    dockerImage = docker.build registry + ":$BUILD_NUMBER" 

                    // Use Jenkins credentials
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credential', usernameVariable: 'datdt185', passwordVariable: 'datdeptraivl123')]) {
                        sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin https://index.docker.io/v1/"
                    }

                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry( 'https://index.docker.io/v1/', 'my-docker-hub-creds' ) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }  
        }
    }
        stage('Deploy') {
            steps {
                echo 'Deploying models..'
                sh "cd k8s/helm/txtsum"
                sh 'helm upgrade --install txtsum'
                echo 'Running a script to trigger pull and start a docker container'
            }
        }
    }
}
