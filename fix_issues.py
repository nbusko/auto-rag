#!/usr/bin/env python3
"""
Скрипт для автоматического исправления основных проблем в AutoRAG системе
"""

import os
import sys
import subprocess
import time
import requests
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutoRAGFixer:
    def __init__(self):
        self.data_service_url = "http://localhost:5050"
        self.rag_service_url = "http://localhost:5060"
        
    def check_docker(self):
        """Проверка наличия Docker"""
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            logger.info("✅ Docker найден")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("❌ Docker не найден. Установите Docker и Docker Compose")
            return False
    
    def check_docker_compose(self):
        """Проверка наличия Docker Compose"""
        try:
            subprocess.run(["docker-compose", "--version"], check=True, capture_output=True)
            logger.info("✅ Docker Compose найден")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("❌ Docker Compose не найден")
            return False
    
    def check_env_file(self):
        """Проверка и создание .env файла"""
        if not os.path.exists(".env"):
            if os.path.exists("env.example"):
                logger.info("Создание .env файла из env.example...")
                subprocess.run(["cp", "env.example", ".env"])
                logger.info("✅ .env файл создан")
                logger.warning("⚠️  Не забудьте настроить OPENAI_API_KEY в .env файле!")
            else:
                logger.error("❌ Файл env.example не найден")
                return False
        else:
            logger.info("✅ .env файл существует")
        return True
    
    def check_openai_key(self):
        """Проверка наличия OpenAI API ключа"""
        try:
            with open(".env", "r") as f:
                content = f.read()
                if "OPENAI_API_KEY=" in content and not "OPENAI_API_KEY=your_api_key_here" in content:
                    logger.info("✅ OpenAI API ключ настроен")
                    return True
                else:
                    logger.warning("⚠️  OpenAI API ключ не настроен в .env файле")
                    return False
        except FileNotFoundError:
            logger.error("❌ .env файл не найден")
            return False
    
    def stop_services(self):
        """Остановка сервисов"""
        logger.info("Остановка сервисов...")
        try:
            subprocess.run(["docker-compose", "down"], check=True)
            logger.info("✅ Сервисы остановлены")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Ошибка остановки сервисов: {e}")
            return False
    
    def build_services(self):
        """Сборка сервисов"""
        logger.info("Сборка сервисов...")
        try:
            subprocess.run(["docker-compose", "build"], check=True)
            logger.info("✅ Сервисы собраны")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Ошибка сборки сервисов: {e}")
            return False
    
    def start_services(self):
        """Запуск сервисов"""
        logger.info("Запуск сервисов...")
        try:
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            logger.info("✅ Сервисы запущены")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Ошибка запуска сервисов: {e}")
            return False
    
    def wait_for_services(self, timeout=60):
        """Ожидание готовности сервисов"""
        logger.info(f"Ожидание готовности сервисов (максимум {timeout} секунд)...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Проверяем Data Service
                response = requests.get(f"{self.data_service_url}/health", timeout=5)
                if response.status_code == 200:
                    logger.info("✅ Data Service готов")
                    
                    # Проверяем RAG Service
                    response = requests.get(f"{self.rag_service_url}/health", timeout=5)
                    if response.status_code == 200:
                        logger.info("✅ RAG Service готов")
                        return True
                    
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(2)
        
        logger.error("❌ Сервисы не готовы в течение отведенного времени")
        return False
    
    def check_swagger(self):
        """Проверка доступности Swagger UI"""
        logger.info("Проверка Swagger UI...")
        
        try:
            # Проверяем Data Service Swagger
            response = requests.get(f"{self.data_service_url}/docs", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Swagger UI Data Service доступен")
            else:
                logger.error(f"❌ Swagger UI Data Service недоступен: {response.status_code}")
                return False
            
            # Проверяем RAG Service Swagger
            response = requests.get(f"{self.rag_service_url}/docs", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Swagger UI RAG Service доступен")
            else:
                logger.error(f"❌ Swagger UI RAG Service недоступен: {response.status_code}")
                return False
            
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Ошибка проверки Swagger UI: {e}")
            return False
    
    def show_logs(self):
        """Показать логи сервисов"""
        logger.info("Логи сервисов:")
        try:
            subprocess.run(["docker-compose", "logs", "--tail=20"])
        except subprocess.CalledProcessError as e:
            logger.error(f"Ошибка получения логов: {e}")
    
    def fix_all(self):
        """Исправление всех проблем"""
        logger.info("🔧 Запуск автоматического исправления проблем...")
        
        # Проверяем предварительные требования
        if not self.check_docker():
            return False
        
        if not self.check_docker_compose():
            return False
        
        if not self.check_env_file():
            return False
        
        # Останавливаем сервисы если они запущены
        self.stop_services()
        
        # Собираем сервисы
        if not self.build_services():
            return False
        
        # Запускаем сервисы
        if not self.start_services():
            return False
        
        # Ждем готовности сервисов
        if not self.wait_for_services():
            logger.error("Сервисы не готовы. Показываем логи:")
            self.show_logs()
            return False
        
        # Проверяем Swagger UI
        if not self.check_swagger():
            logger.error("Swagger UI недоступен. Показываем логи:")
            self.show_logs()
            return False
        
        logger.info("🎉 Все проблемы исправлены!")
        logger.info(f"📖 Swagger UI Data Service: {self.data_service_url}/docs")
        logger.info(f"📖 Swagger UI RAG Service: {self.rag_service_url}/docs")
        
        return True

def main():
    """Основная функция"""
    fixer = AutoRAGFixer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            logger.info("Проверка системы...")
            fixer.check_docker()
            fixer.check_docker_compose()
            fixer.check_env_file()
            fixer.check_openai_key()
            
        elif command == "logs":
            fixer.show_logs()
            
        elif command == "restart":
            logger.info("Перезапуск сервисов...")
            fixer.stop_services()
            fixer.start_services()
            
        else:
            logger.error(f"Неизвестная команда: {command}")
            logger.info("Доступные команды: check, logs, restart")
    else:
        # Автоматическое исправление
        success = fixer.fix_all()
        
        if not success:
            logger.error("❌ Исправление не удалось")
            sys.exit(1)
        else:
            logger.info("✅ Система готова к работе")

if __name__ == "__main__":
    main() 