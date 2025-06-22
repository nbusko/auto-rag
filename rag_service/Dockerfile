FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Обновляем pip
RUN pip install --upgrade pip setuptools wheel

# Копируем и устанавливаем зависимости поэтапно
COPY requirements.txt .

# Устанавливаем базовые зависимости
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv requests

# Устанавливаем ML зависимости
RUN pip install --no-cache-dir numpy sentence-transformers

# Устанавливаем OpenAI и LangChain
RUN pip install --no-cache-dir openai langchain langchain-openai

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5060"] 