# Text Summarization
## Introduction
Our project focuses on implementing text summarization using BART (Bidirectional and Auto-Regressive Transformers), a powerful model developed by Facebook. BART excels in generating coherent and concise summaries by combining both auto-regressive and bidirectional pretraining techniques. Leveraging its state-of-the-art capabilities, our text summarization system aims to distill essential information from lengthy documents, articles, or paragraphs, providing users with succinct and meaningful summaries. This project not only showcases the effectiveness of BART in natural language understanding but also contributes to the advancement of text summarization technology, making information extraction more efficient and accessible.

## Demo
First, install the required packages by running the following command:
```bash 
pip install -r requirements.txt
```

After installing the required packages, you can run the demo by executing the file demo.py:

The result will be displayed in the gradio interface, where you can input the text you want to summarize and get the summarized text as the output.

![image](![alt text](<pic/demo with gradio.png>))

## Running in Docker
To run the demo in a Docker container, you can build the Docker image using the following command:
```bash
docker build -t  name_image .
```

After building the Docker image, you can run the Docker container using the following command:
```bash
docker run -p 30001:30000 name_image
```

![image](![alt text](<pic/Run container app.png>))

Model with deploy in FastAPI with localhost:30001/docs

![image](![alt text](<pic/app run in container.png>))

