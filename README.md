# 🤖 Auto/NoCodeRAG

**Автоматизированная система Retrieval-Augmented Generation (RAG) для обработки документов и генерации ответов на основе контекста**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.13-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai)](https://openai.com/)

## 📋 Содержание

- [🎯 Описание проекта](#-описание-проекта)
- [🏗️ Архитектура](#️-архитектура)
- [🚀 Быстрый старт](#-быстрый-старт)
- [📦 Установка](#-установка)
- [⚙️ Конфигурация](#️-конфигурация)
- [🔧 API Endpoints](#-api-endpoints)
- [📚 Использование](#-использование)
- [🧪 Тестирование](#-тестирование)
- [📊 Мониторинг](#-мониторинг)
- [🤝 Вклад в проект](#-вклад-в-проект)
- [📄 Лицензия](#-лицензия)

## 🎯 Описание проекта

Auto/NoCodeRAG - это современная система для автоматизированной обработки документов и генерации ответов на основе контекста. Проект состоит из двух основных микросервисов:

### 🔍 Document Processor Service
- **Парсинг документов** в различных форматах (PDF, DOCX, XLSX, TXT, DOC, IMGs)
- **Извлечение текста** с поддержкой OCR для изображений
- **Разбиение на чанки** с использованием LLM или batch-метода
- **Генерация эмбеддингов** для семантического поиска
- **Обработка таблиц** с сохранением структуры данных

### 🧠 RAG Service
- **Семантический поиск** по эмбеддингам документов
- **Контекстная генерация** ответов с использованием LLM
- **Настраиваемые промпты** для различных сценариев
- **Поддержка чатов** с историей сообщений
- **Фильтрация по релевантности** с настраиваемым порогом

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    Auto/NoCodeRAG System                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │  Document Processor │    │        RAG Service          │ │
│  │      (Port 5030)    │    │        (Port 5050)          │ │
│  │                     │    │                             │ │
│  │ • Document Parsing  │    │ • Semantic Search           │ │
│  │ • Text Extraction   │    │ • Context Generation        │ │
│  │ • Chunk Splitting   │    │ • LLM Integration           │ │
│  │ • Embedding Gen.    │    │ • Chat Management           │ │
│  └─────────────────────┘    └─────────────────────────────┘ │
│           │                           │                     │
│           └───────────────────────────┘                     │
│                     │                                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 External Services                       │ │
│  │  • OpenAI API (GPT-4o-mini)                            │ │
│  │  • Sentence Transformers (rubert-mini-frida)           │ │
│  │  • OCR Processing                                      │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Технологический стек

- **Backend**: FastAPI, Python 3.8+
- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: Sentence Transformers (rubert-mini-frida)
- **Vector Search**: FAISS
- **Document Processing**: PyPDF2, python-docx, openpyxl, pdf2image
- **Containerization**: Docker & Docker Compose
- **Logging**: Structured logging with JSON format

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- OpenAI API ключ
- Минимум 4GB RAM
- 10GB свободного места на диске

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd auto-rag
```

### 2. Настройка переменных окружения

```bash
cp env.example .env
```

Отредактируйте `.env` файл:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.proxyapi.ru/openai/v1
EMBEDDER_MODEL=sergeyzh/rubert-mini-frida
OCR_MODEL=gpt-4o-mini
```

### 3. Запуск сервисов

```bash
docker-compose up --build
```

### 4. Проверка работоспособности

```bash
# Проверка Document Processor
curl http://localhost:5030/api/v1/health

# Проверка RAG Service
curl http://localhost:5050/api/v1/health
```

## 📦 Установка

### Локальная установка (без Docker)

#### Document Processor Service

```bash
cd document_processor
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python main.py
```

#### RAG Service

```bash
cd rag_service
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python main.py
```

### Установка зависимостей

#### Системные зависимости (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-rus \
    libmagic1 \
    curl
```

#### Python зависимости

Все необходимые зависимости уже включены в `requirements.txt` файлы каждого сервиса.

## ⚙️ Конфигурация

### Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `OPENAI_API_KEY` | Ключ API OpenAI | Обязательно |
| `OPENAI_BASE_URL` | Базовый URL для OpenAI API | `https://api.proxyapi.ru/openai/v1` |
| `EMBEDDER_MODEL` | Модель для генерации эмбеддингов | `sergeyzh/rubert-mini-frida` |
| `OCR_MODEL` | Модель для OCR обработки | `gpt-4o-mini` |

### Настройки сервисов

#### Document Processor (Port 5030)
- **Методы разбиения**: LLM или Batch
- **Размер батча**: 5-2000 символов
- **Поддерживаемые форматы**: PDF, DOCX, XLSX, TXT
- **OCR поддержка**: Да

#### RAG Service (Port 5050)
- **Top-K поиск**: Настраиваемое количество результатов
- **Порог релевантности**: 0.0-1.0
- **Температура генерации**: 0.0-1.0
- **Кастомные промпты**: Поддерживаются

## 🔧 API Endpoints

### Document Processor API

#### `POST /api/v1/documents/process`
Обработка документа и генерация эмбеддингов

**Параметры:**
- `document_id` (UUID): Уникальный идентификатор документа
- `document` (File): Загружаемый файл
- `split_method` (enum): `llm` или `batch`
- `batch_size` (int): Размер батча (5-2000)
- `llm_model` (string): Модель LLM
- `temperature` (float): Температура генерации (0.0-1.0)
- `prompt_split` (string): Промпт для разделения
- `prompt_table` (string): Промпт для таблиц

**Ответ:**
```json
{
  "status": "success",
  "message": "Document processed successfully",
  "document_id": "uuid",
  "texts": ["chunk1", "chunk2", ...],
  "embeddings": [[0.1, 0.2, ...], ...],
  "chunks_count": 10,
  "processing_time": 2.5
}
```

#### `GET /api/v1/health`
Проверка состояния сервиса

### RAG Service API

#### `POST /api/v1/rag/process`
Обработка RAG запроса

**Параметры:**
```json
{
  "chat_id": "string",
  "user_message": "string",
  "document_id": "uuid",
  "message_id": "string",
  "llm": "gpt-4o-mini",
  "prompt_retrieve": "string",
  "prompt_augmentation": "string",
  "prompt_generation": "string",
  "top_k": 12,
  "temperature": 0.7,
  "threshold": 0.0,
  "embeddings": [[0.1, 0.2, ...], ...],
  "text_chunks": ["chunk1", "chunk2", ...]
}
```

**Ответ:**
```json
{
  "status": "success",
  "message": "RAG request processed successfully",
  "chat_id": "string",
  "message_id": "string",
  "document_id": "uuid",
  "generated_answer": "Generated response based on context"
}
```

#### `GET /api/v1/health`
Проверка состояния сервиса

## 📚 Использование

### Пример работы с API

#### 1. Обработка документа

```python
import requests
import uuid

# Загрузка и обработка документа
document_id = str(uuid.uuid4())
files = {'document': open('document.pdf', 'rb')}
data = {
    'document_id': document_id,
    'split_method': 'llm',
    'llm_model': 'gpt-4o-mini',
    'temperature': 0.1
}

response = requests.post(
    'http://localhost:5030/api/v1/documents/process',
    files=files,
    data=data
)

result = response.json()
texts = result['texts']
embeddings = result['embeddings']
```

#### 2. RAG запрос

```python
# Генерация ответа на основе контекста
rag_request = {
    'chat_id': 'user123',
    'user_message': 'Какие основные темы обсуждаются в документе?',
    'document_id': document_id,
    'embeddings': embeddings,
    'text_chunks': texts,
    'top_k': 5,
    'temperature': 0.7
}

response = requests.post(
    'http://localhost:5050/api/v1/rag/process',
    json=rag_request
)

answer = response.json()['generated_answer']
print(f"Ответ: {answer}")
```

### Интеграция с внешними системами

#### cURL примеры

```bash
# Обработка документа
curl -X POST "http://localhost:5030/api/v1/documents/process" \
  -F "document_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "document=@document.pdf" \
  -F "split_method=llm"

# RAG запрос
curl -X POST "http://localhost:5050/api/v1/rag/process" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "user123",
    "user_message": "Вопрос по документу",
    "document_id": "123e4567-e89b-12d3-a456-426614174000",
    "embeddings": [[0.1, 0.2, 0.3]],
    "text_chunks": ["Текст документа"]
  }'
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Тестирование Document Processor
python test_document_processor.py

# Тестирование RAG Service
python test_service.py
```

### Проверка работоспособности

```bash
# Проверка всех сервисов
docker-compose ps

# Просмотр логов
docker-compose logs -f

# Проверка здоровья сервисов
curl http://localhost:5030/api/v1/health
curl http://localhost:5050/api/v1/health
```

## 📊 Мониторинг

### Логирование

Все сервисы используют структурированное логирование в формате JSON:

```bash
# Просмотр логов Document Processor
docker-compose logs document_processor

# Просмотр логов RAG Service
docker-compose logs rag_service
```

### Метрики

- Время обработки документов
- Количество созданных чанков
- Время ответа RAG запросов
- Использование памяти и CPU

### Health Checks

Сервисы автоматически проверяют свое состояние каждые 30 секунд:

```bash
# Ручная проверка здоровья
curl http://localhost:5030/api/v1/health
curl http://localhost:5050/api/v1/health
```

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста, следуйте этим шагам:

1. **Fork** репозитория
2. Создайте **feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** изменения (`git commit -m 'Add amazing feature'`)
4. **Push** в branch (`git push origin feature/amazing-feature`)
5. Откройте **Pull Request**

### Стандарты кода

- Следуйте PEP 8 для Python кода
- Добавляйте типы для всех функций
- Пишите документацию для новых API endpoints
- Добавляйте тесты для новой функциональности


## 🔗 Полезные ссылки

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Sentence Transformers](https://www.sbert.net/)
- [FAISS Documentation](https://faiss.ai/)

## 📞 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте [Issues](../../issues) на GitHub
2. Создайте новое issue с подробным описанием проблемы
3. Укажите версии используемых компонентов и логи ошибок

---

**Сделано с ❤️ для автоматизации RAG систем**
