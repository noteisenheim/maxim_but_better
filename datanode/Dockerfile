FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add git && rm -rf /var/cache/apk/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD python datanode1.py
