from typing import Optional

from fastapi import FastAPI
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# Initialize the summarizer

model_dir = "model/"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)


app = FastAPI(root_path="/txtapp-service")


@app.get("/Text_Summarization")
def text_summarization(text: Optional[str] = None):
    results = {"Mlops": [{"Author": "DrissDo"}]}
    if text:
        # Use the summarizer to summarize the text
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        results.update({"Text Summarization ": summary})
    return results
