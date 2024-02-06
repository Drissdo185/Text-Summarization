FROM python:3.11


WORKDIR /app


COPY ./main.py /app

COPY ./requirements.txt /app

COPY ./k8s /app

EXPOSE 30000


RUN pip install -r requirements.txt --no-cache-dir

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]