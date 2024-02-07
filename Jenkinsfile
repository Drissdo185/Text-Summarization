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
                script {
                    
                    sh "docker pull ${registry}:${BUILD_NUMBER}"

                    
                    dir('k8s/helm/txtsum') {
                        sh 'helm upgrade --install txtsum .'
                    }
                }
            }
        }   
    }
}