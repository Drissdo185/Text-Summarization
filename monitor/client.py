from time import sleep
import requests
from loguru import logger

def predict():
    logger.info("Sending GET requests!")
    params = {
        "Text": "Your text to summarize goes here",
    }
    response = requests.get(
        "http://localhost:8000/Text_Summarization",
        headers={
            "accept": "application/json",
        },
        params=params,
    )
    print(response.json())

if __name__ == "__main__":
    while True:
        predict()
        sleep(0.5)