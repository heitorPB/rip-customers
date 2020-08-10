FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app
