# Text Summarization
## Introduction
Our project focuses on implementing text summarization using BART (Bidirectional and Auto-Regressive Transformers), a powerful model developed by Facebook. BART excels in generating coherent and concise summaries by combining both auto-regressive and bidirectional pretraining techniques. Leveraging its state-of-the-art capabilities, our text summarization system aims to distill essential information from lengthy documents, articles, or paragraphs, providing users with succinct and meaningful summaries. This project not only showcases the effectiveness of BART in natural language understanding but also contributes to the advancement of text summarization technology, making information extraction more efficient and accessible.



# Table of Contents
1. [Text Summarization](#text-summarization)
   1. [Introduction](#introduction)
   2. [Project Structure](#structure)
2. [Local](#local)
   1. [Demo](#demo)
   2. [Running in Docker](#running-in-docker)
   3. [Monitoring](#monitoring)
   4. [CI/CD](#cicd)
3. [Cloud](#cloud)
   1. [Deploying to GCP](#deploying-to-gcp)
   2. [CICD with Jenkins for GCE](#cicd-with-jenkins-for-gce)




## Project Structure
```txt
├── demo.ipynb                - Jupyter notebook for running the demo
├── docker-compose.yaml       - Docker Compose configuration file
├── Dockerfile                - Dockerfile for building the image
├── env                       - Directory for environment variables
├── helm                      - Directory for Helm chart to deploy the application
├── images                    - Directory for image files
├── jenkins                   - Directory for Jenkins configuration files
├── Jenkinsfile               - Jenkins pipeline script to describe the CI/CD process
├── local                     - Directory for local contain Ansible to build GCE
├── main.py                   - Main Python script for the application
├── model                     - Directory for model files
├── monitor                   - Directory for monitoring such as Elasticsearch, Kibana, Prometheus, Grafana
├── README.md                 - This README file
├── requirements.txt          - Python requirements file
└── terraform                 - Directory for Terraform to build GKE
```


# Local
![image alt text](<images/Local.png>)
### Demo
First, install the required packages by running the following command:\
Python Version: 3.11.6
```bash
pip install -r requirements.txt
```

After installing the required packages, you can run the demo by executing the file demo.ipynb:

The result will be displayed in the gradio interface, where you can input the text you want to summarize and get the summarized text as the output.

![image alt text](<images/demo with gradio.png>)

### Running in Docker
To run the demo in a Docker container, you can build the Docker image using the following command:
```bash
docker build -t  name_image .
```

After building the Docker image, you can run the Docker container using the following command:
```bash
docker run -p 30001:30000 name_image
```

![image alt text](<images/Run container app.png>)

Model with deploy in FastAPI with localhost:30001/docs

![image alt text](<images/app run in container.png>)

### Monitoring
To monitor the system, you can use Prometheus and Grafana. First, start the Prometheus and Grafana services by running the following command:
```bash
cd monitor
docker compose -f prom-graf-docker-compose.yaml up -d
```

Access the Prometheus dashboard at localhost:9090 and Grafana dashboard at localhost:3000. The default username and password for Grafana are admin and admin, respectively.

![image alt text](<images/gafanademo.png>)

## CI/CD
We have two stages, build and deploy, in our CI/CD pipeline. The build stage is responsible for building the Docker image, while the deploy stage is responsible for deploying the Docker image to the cloud. We use GitHub Actions to automate the CI/CD pipeline. The pipeline is triggered whenever a new commit is pushed to the main branch.
```bash
cd jenkins
docker build -t yourname/jenkins . # create image
docker compose -f dokcer-compose.yaml up -d # remember to change the name of image in docker-compose.yaml
```
Access the Jenkins dashboard at localhost:8080. The default username is admin. You can get the password by running the following command:
```bash
docker logs jenkins
```
After logging in, you have to install some plugins

* Docker
* Docker Pipeline
* Docker API

More over use have to set the credentials for Docker Hub
* Docker Credentials
* Git Credentials (using ngrok to expose the local server to the internet)


![image alt text](</images/DemoCICD.png>)

# Cloud
![image alt text](</images/Cloud.png>)
## Deploying to GCP
Now, we will deploy the model to the cloud using GCP. First, you need to create a project and enable the Compute Engine and Kubernetes Engine APIs. Then, you can deploy the model to GKE using the following command:

* [Install gcloud CLI](https://cloud.google.com/sdk/docs/install#deb)

* Install gke-gcloud-auth-plugin

```bash
sudo apt-get install google-cloud-cli-gke-gcloud-auth-plugin
```
* Set GCloud Project

 Authorizes gcloud and other SDK tools to access Google Cloud and setup configuration
```bash
gcloud init
```
* Login to GCP
```bash
gcloud auth application-default login
```
* Deploy model to Google Kubernetes Engine (GKE)
    * Using terraform to create a GKE cluster
```bash
cd terraform
terraform init
terraform plan # please check the plan before applying
terraform apply
```


* Connect to GKE

![image alt text](</images/GKE1.png>)

Copy the command and run it in the terminal
```bash
gcloud container clusters get-credentials mlops-414313-gke --region us-central1 --project mlops-414313
```
Using command kubectx to check right context, if it is not right, you can change it by using command kubectx <context_name>


![image alt text](</images/GKE2.png>)

* Create necessary namespaces
```bash
kubectl create ns model-serving
kubectl create ns monitoring
kubectl create ns nginx-ingress
```

* Deploy nginx ingress controller
```bash
cd helm/nginx-ingress
helm upgrade --install nginx-ingress helm_charts/nginx-ingress -n nginx-ingress
```
* Deploy application to GKE
```bash
helm upgrade --install txtapp helm_charts/txtapp -n model-serving
```
* Update Domain Name
```bash
sudo nano /etc/hosts
external_ip txtapp.example.com # external_ip is the external ip of nginx-ingress-controller)
```
![image alt text](</images/GKE3.png>)


## CICD with Jenkins for GCE
To automate the CI/CD pipeline for deploying the model to GKE with Jenkins, we will have some setup steps as follows:
First, we should enable the Google Compute Engine and Google Kubernetes Engine APIs in the GCP console.

![image alt text](</images/GCE.png>)

![image alt text](</images/GCE2.png>)


We will use Ansible to create GCE.
First, we will set up the environment for Ansible and connect to GCE.
Access to here to generate the key to connect to GCE
![image alt text](</images/Ansible.png>)
Access to project which you want to connect to GCE
Then click the manage key and select JSON

![image alt text](</images/Ansibl2.png>)

Remember keep the key in the safe place and do not share it with anyone. (In my project I keep it in the folder ansible/secretes/)
Then we will use the key to connect to GCE.
### Create the Compute Engine
```bash
ansible-playbook create_compute_instance.yaml
```
Copy the external ip of the GCE and put it in file inventory

### Create the key
```bash
ssh-keygen
cat ~/.ssh/id_rsa.pub # copy the key and add it to the GCE
```
![image alt text](</images/GCE4.png>)

Alright, now we have the GCE, we will use Ansible to install Jenkins and Docker in the VM.

```bash
ansible-playbook -i ../inventory deploy_jenkins.yaml
```

![image alt text](</images/ansible4.png>)

Now, we can access the Jenkins dashboard at the

external ip:8081

* Install the necessary plugins
Same plugins as we did in the local Jenkins. More over, we have to install:
    * Kubernetes Client API plugin
    * Kubernetes Credentials plugin
    * Kubernets Plugin
    * GCloud SDK plugin

And few settings in Jenkins
Manage Jenkins -> Node and Cloud -> Configure Clouds -> Add a new cloud -> Kubernetes

Fill the information as below
* Kubernetes URL: https://external_ip
* Kubernetes server certificate key get from
```bash
cat ~/.kube/config
```
![image alt text](</images/aaa.png>)

* Jenkins URL: http://external_ip:8081

Then click test connection to check the connection
It will show error, we will fix it with
```bash
kubectl create clusterrolebinding cluster-admin-binding --clusterrole cluster-admin --user $(gcloud config get-value account)
```

![image alt text](</images/DeployGKE.png>)

Save it and build the pipeline.
![image alt text](</images/JenkinsGCE.png>)
