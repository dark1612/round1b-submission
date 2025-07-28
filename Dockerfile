# Dockerfile
FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

COPY app /app

RUN pip install --no-cache-dir PyMuPDF==1.23.7

CMD ["python", "main.py"]
