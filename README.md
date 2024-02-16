# Text Summarization
## Introduction
Our project focuses on implementing text summarization using BART (Bidirectional and Auto-Regressive Transformers), a powerful model developed by Facebook. BART excels in generating coherent and concise summaries by combining both auto-regressive and bidirectional pretraining techniques. Leveraging its state-of-the-art capabilities, our text summarization system aims to distill essential information from lengthy documents, articles, or paragraphs, providing users with succinct and meaningful summaries. This project not only showcases the effectiveness of BART in natural language understanding but also contributes to the advancement of text summarization technology, making information extraction more efficient and accessible.

## Local
### Demo
First, install the required packages by running the following command:
```bash 
pip install -r requirements.txt
```

After installing the required packages, you can run the demo by executing the file demo.ipynb:

The result will be displayed in the gradio interface, where you can input the text you want to summarize and get the summarized text as the output.

![image alt text](<pic/demo with gradio.png>)

### Running in Docker
To run the demo in a Docker container, you can build the Docker image using the following command:
```bash
docker build -t  name_image .
```

After building the Docker image, you can run the Docker container using the following command:
```bash
docker run -p 30001:30000 name_image
```

![image alt text](<pic/Run container app.png>)

Model with deploy in FastAPI with localhost:30001/docs

![image alt text](<pic/app run in container.png>)

### Monitoring
To monitor the system, you can use Prometheus and Grafana. First, start the Prometheus and Grafana services by running the following command:
```bash
docker compose -f prom-graf-docker-compose.yaml up -d
```

Access the Prometheus dashboard at localhost:9090 and Grafana dashboard at localhost:3000. The default username and password for Grafana are admin and admin, respectively.

![image alt text](<pic/gafanademo.png>)

## Cloud
Now, we will deploy the model to the cloud using GCP. First, you need to create a project and enable the Compute Engine and Kubernetes Engine APIs. Then, you can deploy the model to GKE using the following command:

* [Install gcloud CLI](https://cloud.google.com/sdk/docs/install#deb)

* Install gke-gcloud-auth-plugin

```bash
sudo apt-get install google-cloud-cli-gke-gcloud-auth-plugin
```
* Set GCloud Project
    * Authorizes gcloud and other SDK tools to access Google Cloud and setup configuration
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


* Connect t to GKE

![image alt text](</pic/GKE1.png>)

Copy the command and run it in the terminal
```bash
gcloud container clusters get-credentials mlops-414313-gke --region us-central1 --project mlops-414313
```
Using command kubectx to check right context, if it is not right, you can change it by using command kubectx <context_name>


![image alt text](</pic/GKE2.png>)

* Create necessary namespaces
```bash
kubectl create ns model-serving
kubectl create ns monitoring
kubectl create ns nginx-ingress
```

* Deploy nginx ingress controller
```bash
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
![image alt text](</pic/GKE3.png>)    



