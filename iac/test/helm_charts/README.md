## How-to Guide
### Deploy and connect to a cluster

### Install the chart for our OCR without ingress
```shell
cd ocr_wo_ingress
kubectl create ns model-serving
helm upgrade --install ocr . -n model-serving
```
,then use the following command to get the `EXTERNAL-IP`
```
kubectl get svc -n model-serving
```
, assume that the `EXTERNAL-IP` you have found is `104.154.48.94`, open your browser and type `http://104.154.48.94:30000/docs`

### Install the chart for our OCR with NGINX ingress
First, install the NGINX chart, which was downloaded from [here](https://docs.nginx.com/nginx-ingress-controller/installation/installation-with-helm/#managing-the-chart-via-sources).
```shell
kubectl create ns nginx-ingress # Create a new namespace
kubens nginx-ingress # Switch to the new namespace
cd nginx-ingress
helm upgrade --install nginx-ingress-controller .
```
, then install the OCR chart
```shell
cd ocr_ingress
helm upgrade --install ocr . -n model-serving
```
Next, get `ocr-nginx-ingress`'s `External IP` by the following command
```shell
kubectl get ing -n model-serving
```
Continue by mapping the host `ocr.example.com` to the `External IP`, assume that the IP is `34.27.189.190`, then add the following line to the file `/etc/hosts`

```shell
sudo sh -c 'echo "34.27.189.190 ocr.example.com" >> /etc/hosts'
```
Finally, open your browser and access `http://ocr.example.com/docs`