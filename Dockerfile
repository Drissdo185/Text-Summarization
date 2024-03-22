FROM python:3.11


WORKDIR /app

RUN mkdir /app/mode

COPY ./requirements.txt /app

RUN pip install -r requirements.txt --no-cache-dir

COPY ./model /app/model

COPY ./main.py /app

EXPOSE 30000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]
