import logging
import os
from datetime import datetime

def setup_logging():
    # Создаем директорию для логов если её нет
    os.makedirs('logs', exist_ok=True)
    
    # Настраиваем формат логов
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Настраиваем корневой логгер
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(),  # Вывод в консоль
            logging.FileHandler('logs/rag_service.log', encoding='utf-8')  # Вывод в файл
        ]
    )
    
    # Настраиваем логгеры для внешних библиотек
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('fastapi').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.INFO)
    
    # Логируем запуск
    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized")