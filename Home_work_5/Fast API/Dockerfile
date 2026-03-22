# 🐳 Dockerfile для FastAPI приложения
# 🚀 Запуск:
#    docker build -t my-fastapi-app .
#    docker run -p 8001:8001 my-fastapi-app

FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --default-timeout=100 --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Копируем весь исходный код
COPY app/ ./app/

# Открываем порт
EXPOSE 8001

# Запускаем приложение
# ⚠️ --host 0.0.0.0 обязателен для доступа извне контейнера!
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]