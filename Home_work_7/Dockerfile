FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --index-url https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . .

# Gunicorn запускает Flask в production-режиме
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "--workers", "4", "app:create_app()"]