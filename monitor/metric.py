from io import BytesIO
from typing import Optional

import easyocr
import numpy as np
import uvicorn
from loguru import logger
from time import time
from fastapi import FastAPI, File, UploadFile
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from PIL import Image
from prometheus_client import start_http_server
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Start Prometheus client
start_http_server(port=8099, addr="0.0.0.0")

# Service name is required for most backends
resource = Resource(attributes={SERVICE_NAME: "ocr-service"})

# Exporter to export metrics to Prometheus
reader = PrometheusMetricReader()

# Meter is responsible for creating and recording metrics
provider = MeterProvider(resource=resource, metric_readers=[reader])
set_meter_provider(provider)
meter = metrics.get_meter("myapp", "1.0.0")

# Create your first counter
counter = meter.create_counter(
    name="App_request_counter",
    description="Number of app requests"
)

histogram = meter.create_histogram(
    name="App_response_histogram",
    description="App response histogram",
    unit="seconds",
)

model_dir = "/model/"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

app = FastAPI(
    root_path="/txtapp-service"
)

@app.get("/Text_Summarization")
async def text_summarization(Text: Optional[str] = None):
    results = {"Mlops": [{"Author": "DrissDo"}]}
    if Text:
        # Use the summarizer to summarize the text
        summary = summarizer(Text, max_length=130, min_length=30, do_sample=False)
        results.update({"Text Summarization ": summary})

    
    # Labels for all metrics
    label = {"api": "/app"}

    # Increase the counter
    counter.add(10, label)

    # Mark the start and end of the response
    starting_time = time()
    # ... your code to process the request here ...
    ending_time = time()
    elapsed_time = ending_time - starting_time

    # Add histogram
    logger.info("elapsed time: ", elapsed_time)
    logger.info(elapsed_time)
    histogram.record(elapsed_time, label)
    return results


 