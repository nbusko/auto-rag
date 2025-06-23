# AutoRAG

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)

**Платформа для создания RAG (Retrieval-Augmented Generation) систем**

</div>

## 📋 Описание

AutoRAG - это сервис для обработки RAG запросов и генерации ответов на основе контекста. Система использует векторный поиск для нахождения релевантных документов и генерирует ответы с помощью LLM.

## 🏗️ Архитектура

Система состоит из двух основных компонентов:

- **PostgreSQL с pgvector** - база данных с расширением для векторного поиска
- **RAG Service** - FastAPI сервис для обработки RAG запросов и генерации ответов

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- OpenAI API ключ (или совместимый прокси)

### 1. Настройка окружения

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd auto-rag

# Создайте .env файл из примера
cp env.example .env

# Настройте OPENAI_API_KEY в .env файле
# OPENAI_API_KEY=your_api_key_here
```

### 2. Запуск системы

```bash
docker-compose up --build
```

## 📚 API Endpoints

### RAG Service (http://localhost:5060)

- `GET /api/v1/` - Информация о сервисе
- `GET /api/v1/health` - Проверка здоровья
- `GET /docs` - Swagger UI
- `POST /api/v1/rag/process` - Обработать RAG запрос

### Пример запроса к RAG API

```bash
curl -X POST "http://localhost:5060/api/v1/rag/process" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "user123",
    "user_message": "Что такое машинное обучение?",
    "document_id": "doc123",
    "embeddings": [[0.1, 0.2, ...], [0.3, 0.4, ...]],
    "text_chunks": ["Машинное обучение - это...", "ИИ включает в себя..."]
  }'
```

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `OPENAI_API_KEY` | Ключ API OpenAI | - |
| `OPENAI_BASE_URL` | URL API OpenAI | `https://api.proxyapi.ru/openai/v1` |
| `EMBEDDER_MODEL` | Модель для эмбеддингов | `sergeyzh/rubert-mini-frida` |

### Настройка модели

Система поддерживает различные модели для:
- **Эмбеддинги**: sentence-transformers модели
- **LLM**: OpenAI GPT модели

## 📁 Структура проекта

```
auto-rag/
├── rag_service/              # RAG сервис
│   ├── main.py              # Основной файл FastAPI
│   ├── router.py            # API роуты
│   ├── rag_pipeline.py      # RAG пайплайн
│   ├── embedding_search.py  # Поиск по эмбеддингам
│   ├── config/              # Конфигурация
│   │   ├── contracts.py     # Pydantic модели
│   │   ├── constants.py     # Константы и промпты
│   │   ├── rag_settings.py  # Настройки приложения
│   │   └── logger.py        # Настройка логирования
│   ├── requirements.txt     # Python зависимости
│   └── Dockerfile          # Docker образ
├── docker-compose.yml      # Конфигурация Docker
├── Makefile               # Команды управления
├── env.example           # Пример переменных окружения
└── README.md            # Документация
```

## 🔍 Логирование

Все сервисы настроены с подробным логированием:

- Логи выводятся в консоль и в файлы:
  - `logs/rag_service.log` - логи RAG Service

## 📊 Мониторинг

- **Health Check**: `GET /api/v1/health`
- **Swagger UI**: `GET /docs`
- **Логи**: `make logs-rag`

## 🔒 Безопасность

- Все API ключи хранятся в переменных окружения
- CORS настроен для разработки (настройте для продакшена)
- Валидация входных данных через Pydantic

---

<div align="center">

**AutoRAG** - Умные ответы на основе контекста

</div>
