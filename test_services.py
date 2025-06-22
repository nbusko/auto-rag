#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы RAG и Data сервисов
"""

import requests
import json
import time
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Конфигурация
DATA_SERVICE_URL = "http://localhost:5050"
RAG_SERVICE_URL = "http://localhost:5060"

def test_data_service():
    """Тестирование Data Service"""
    logger.info("=== Тестирование Data Service ===")
    
    try:
        # Проверка доступности сервиса
        response = requests.get(f"{DATA_SERVICE_URL}/health", timeout=10)
        if response.status_code == 200:
            logger.info("✅ Data Service доступен")
        else:
            logger.error(f"❌ Data Service недоступен: {response.status_code}")
            return False
        
        # Проверка Swagger UI
        response = requests.get(f"{DATA_SERVICE_URL}/docs", timeout=10)
        if response.status_code == 200:
            logger.info("✅ Swagger UI Data Service доступен")
        else:
            logger.error(f"❌ Swagger UI Data Service недоступен: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Ошибка подключения к Data Service: {e}")
        return False

def test_rag_service():
    """Тестирование RAG Service"""
    logger.info("=== Тестирование RAG Service ===")
    
    try:
        # Проверка доступности сервиса
        response = requests.get(f"{RAG_SERVICE_URL}/health", timeout=10)
        if response.status_code == 200:
            logger.info("✅ RAG Service доступен")
        else:
            logger.error(f"❌ RAG Service недоступен: {response.status_code}")
            return False
        
        # Проверка Swagger UI
        response = requests.get(f"{RAG_SERVICE_URL}/docs", timeout=10)
        if response.status_code == 200:
            logger.info("✅ Swagger UI RAG Service доступен")
        else:
            logger.error(f"❌ Swagger UI RAG Service недоступен: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Ошибка подключения к RAG Service: {e}")
        return False

def test_services_integration():
    """Тестирование интеграции сервисов"""
    logger.info("=== Тестирование интеграции сервисов ===")
    
    try:
        # Создаем тестовый чат
        chat_id = "test_chat_123"
        
        # Добавляем параметры чата через Data Service
        params_data = {
            "chat_id": chat_id,
            "prompt_id": "test_prompt",
            "document_id": "test_doc",
            "top_k": 3,
            "temperature": 0.7,
            "max_tokens": 1000,
            "model_name": "gpt-3.5-turbo"
        }
        
        response = requests.post(f"{DATA_SERVICE_URL}/chat/{chat_id}/params", 
                               json=params_data, timeout=10)
        if response.status_code == 200:
            logger.info("✅ Параметры чата добавлены")
        else:
            logger.error(f"❌ Ошибка добавления параметров: {response.status_code}")
            return False
        
        # Добавляем тестовый документ
        doc_data = {
            "document_id": "test_doc",
            "content": "Это тестовый документ для проверки работы RAG системы. Он содержит информацию о различных технологиях и методах обработки данных.",
            "chunk_size": 100,
            "chunk_overlap": 20
        }
        
        response = requests.post(f"{DATA_SERVICE_URL}/docs/update", 
                               json=doc_data, timeout=30)
        if response.status_code == 200:
            logger.info("✅ Тестовый документ добавлен")
        else:
            logger.error(f"❌ Ошибка добавления документа: {response.status_code}")
            return False
        
        # Тестируем RAG запрос
        rag_request = {
            "chat_id": chat_id,
            "user_message": "Что содержит тестовый документ?"
        }
        
        response = requests.post(f"{RAG_SERVICE_URL}/rag/process", 
                               json=rag_request, timeout=30)
        if response.status_code == 200:
            result = response.json()
            logger.info("✅ RAG запрос обработан успешно")
            logger.info(f"Ответ ассистента: {result.get('assistant_message', '')[:100]}...")
        else:
            logger.error(f"❌ Ошибка RAG запроса: {response.status_code}")
            logger.error(f"Детали: {response.text}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Ошибка интеграционного теста: {e}")
        return False

def main():
    """Основная функция тестирования"""
    logger.info("Запуск тестирования сервисов...")
    
    # Ждем немного для запуска сервисов
    logger.info("Ожидание запуска сервисов...")
    time.sleep(5)
    
    # Тестируем каждый сервис отдельно
    data_service_ok = test_data_service()
    rag_service_ok = test_rag_service()
    
    if data_service_ok and rag_service_ok:
        # Тестируем интеграцию
        integration_ok = test_services_integration()
        
        if integration_ok:
            logger.info("🎉 Все тесты прошли успешно!")
            logger.info(f"📖 Swagger UI Data Service: {DATA_SERVICE_URL}/docs")
            logger.info(f"📖 Swagger UI RAG Service: {RAG_SERVICE_URL}/docs")
        else:
            logger.error("❌ Интеграционные тесты не прошли")
    else:
        logger.error("❌ Один или несколько сервисов недоступны")

if __name__ == "__main__":
    main() 