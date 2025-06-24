#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы RAG сервиса
"""

import requests
import time
import sys
import uuid

def test_health_check():
    """Тест health check эндпоинта"""
    print("🔍 Тестирование health check...")
    try:
        response = requests.get("http://localhost:5050/api/v1/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check успешен")
            print(f"   Ответ: {response.json()}")
            return True
        else:
            print(f"❌ Health check неуспешен: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_root_endpoint():
    """Тест корневого эндпоинта"""
    print("\n🔍 Тестирование корневого эндпоинта...")
    try:
        response = requests.get("http://localhost:5050/api/v1/", timeout=10)
        if response.status_code == 200:
            print("✅ Корневой эндпоинт работает")
            print(f"   Ответ: {response.json()}")
            return True
        else:
            print(f"❌ Корневой эндпоинт не работает: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_rag_process():
    """Тест RAG process эндпоинта"""
    print("\n🔍 Тестирование RAG process...")
    
    # Тестовые данные
    test_data = {
        "chat_id": str(uuid.uuid4()),
        "user_message": "Что такое искусственный интеллект?",
        "document_id": str(uuid.uuid4()),
        "embeddings": [[0.5] * 312],  # Тестовый эмбеддинг размерности 312
        "text_chunks": ["Искусственный интеллект это нейросеть на стероидах" * 312],
        "top_k": 5,
        "temperature": 0.7,
        "threshold": 0.0
    }
    
    try:
        response = requests.post(
            "http://localhost:5050/api/v1/rag/process",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ RAG process работает")
            print(f"   Статус: {result.get('status')}")
            print(f"   Сообщение: {result.get('message')}")
            if result.get('generated_answer'):
                print(f"   Ответ: {result.get('generated_answer')[:100]}...")
            return True
        else:
            print(f"❌ RAG process не работает: {response.status_code}")
            print(f"   Ошибка: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_swagger_ui():
    """Тест доступности Swagger UI"""
    print("\n🔍 Тестирование Swagger UI...")
    try:
        response = requests.get("http://localhost:5050/docs", timeout=10)
        if response.status_code == 200:
            print("✅ Swagger UI доступен")
            return True
        else:
            print(f"❌ Swagger UI недоступен: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов RAG сервиса...")
    print("=" * 50)
    
    # Ждем немного для запуска сервиса
    print("⏳ Ожидание запуска сервиса...")
    time.sleep(5)
    
    tests = [
        test_health_check,
        test_root_endpoint,
        test_swagger_ui,
        test_rag_process
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Небольшая пауза между тестами
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты тестирования: {passed}/{total} тестов прошли успешно")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно! Сервис работает корректно.")
        return 0
    else:
        print("⚠️  Некоторые тесты не прошли. Проверьте логи сервиса.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 