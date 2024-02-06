pipeline {
    agent any

    options{
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment{
        registry = 'datdt185/text_summarization'
        registryCredential = 'dockerhub'      
    }

    stages {
        stage('Preparation') {
            agent {
                docker {
                    image 'python:3.11' 
                }
            }
            steps {
                echo 'Installing dependencies..'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Build') {
            steps {
                script {
                    echo 'Building image for deployment..'
                    dockerImage = docker.build registry + ":$BUILD_NUMBER" 
                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                        dockerImage.push('latest')
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