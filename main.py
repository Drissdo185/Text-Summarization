from fastapi import FastAPI
from typing import Optional
from transformers import pipeline

# Initialize the summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

app = FastAPI()

@app.get("/Text_Summarization")
async def text_summarization(Text: Optional[str] = None):
    results = {"Mlops": [{"Author": "DrissDo"}]}
    if Text:
        # Use the summarizer to summarize the text
        summary = summarizer(Text, max_length=130, min_length=30, do_sample=False)
        results.update({"Text Summarization ": summary})
    return results