FROM python:3.11-slim
RUN pip install fastapi uvicorn[standard]
WORKDIR /app
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]