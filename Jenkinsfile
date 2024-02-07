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
        stage('Deploy to Google Kubernetes Engine') {
            agent {
                kubernetes {
                    containerTemplate {
                        name 'gracious_mayer' // Name of the container to be used for helm upgrade
                        image 'datdt185/helm' // The image containing helm
                    }
                }
            }
            steps {
                script {
                    container('helm') {
                        sh("helm upgrade --install app --set image.repository=${registry} \
                        --set image.tag=v1.${BUILD_NUMBER} ./k8s/helm_charts/txtsum_chart --namespace model-serving")
                    }
                }
            }
        }        
    }
}