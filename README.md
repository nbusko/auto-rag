# 🤖 AutoRAG - Интеллектуальная система RAG

**Полнофункциональная система Retrieval-Augmented Generation с веб-интерфейсом на Blazor и микросервисной архитектурой**

[![.NET](https://img.shields.io/badge/.NET-8.0-512BD4?style=for-the-badge&logo=.net)](https://dotnet.microsoft.com/)
[![Blazor](https://img.shields.io/badge/Blazor-Server-512BD4?style=for-the-badge&logo=blazor)](https://blazor.net/)
[![MudBlazor](https://img.shields.io/badge/MudBlazor-UI-512BD4?style=for-the-badge)](https://mudblazor.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.13-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![pgvector](https://img.shields.io/badge/pgvector-Vector-336791?style=for-the-badge)](https://github.com/pgvector/pgvector)
[![MinIO](https://img.shields.io/badge/MinIO-Object%20Storage-FF0000?style=for-the-badge&logo=minio)](https://min.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai)](https://openai.com/)

## 📋 Содержание

- [🎯 Описание проекта](#-описание-проекта)
- [🏗️ Архитектура системы](#️-архитектура-системы)
- [🔧 Технологический стек](#-технологический-стек)
- [📁 Структура проекта](#-структура-проекта)
- [🚀 Быстрый старт](#-быстрый-старт)
- [⚙️ Конфигурация](#️-конфигурация)
- [🔌 API Endpoints](#-api-endpoints)
- [📚 Использование](#-использование)
- [🧪 Тестирование](#-тестирование)
- [📊 Мониторинг](#-мониторинг)
- [🤝 Вклад в проект](#-вклад-в-проект)
- [📄 Лицензия](#-лицензия)

## 🎯 Описание проекта

AutoRAG - это современная система для автоматизированной обработки документов и генерации интеллектуальных ответов на основе контекста. Проект объединяет мощь микросервисной архитектуры с элегантным веб-интерфейсом, построенным на принципах Clean Architecture и MVVM.

### 🌟 Ключевые возможности

- **📄 Многоформатная обработка документов** (PDF, DOCX, XLSX, TXT, изображения с OCR)
- **🧠 Интеллектуальный семантический поиск** с использованием векторных эмбеддингов
- **💬 Интерактивный чат-интерфейс** с историей сообщений
- **⚙️ Настраиваемые RAG-конфигурации** для различных сценариев
- **👥 Система аутентификации и управления пользователями**
- **📊 Аналитика и годовые данные**
- **🔗 Система шаринга** документов и конфигураций
- **☁️ Облачное хранение** файлов с MinIO
- **🔍 Векторный поиск** с PostgreSQL и pgvector

## 🏗️ Архитектура системы

### Общая архитектура

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AutoRAG System                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                        Web Application (Blazor)                            │ │
│  │                              Port: 8080                                    │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │ │
│  │  │   Auth      │ │    Chat     │ │ Documents   │ │   Settings  │           │ │
│  │  │   Page      │ │    Page     │ │   Page      │ │    Page     │           │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                            │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                        Microservices Layer                                 │ │
│  │                                                                            │ │
│  │  ┌─────────────────────┐    ┌─────────────────────────────┐                │ │
│  │  │  Document Processor │    │        RAG Service          │                │ │
│  │  │      (Port 5030)    │    │        (Port 5050)          │                │ │
│  │  │                     │    │                             │                │ │
│  │  │ • Document Parsing  │    │ • Semantic Search           │                │ │
│  │  │ • Text Extraction   │    │ • Context Generation        │                │ │
│  │  │ • Chunk Splitting   │    │ • LLM Integration           │                │ │
│  │  │ • Embedding Gen.    │    │ • Chat Management           │                │ │
│  │  └─────────────────────┘    └─────────────────────────────┘                │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                            │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                        Infrastructure Layer                                │ │
│  │                                                                            │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │ │
│  │  │ PostgreSQL  │ │    MinIO    │ │   OpenAI    │ │  External   │           │ │
│  │  │ + pgvector  │ │   Storage   │ │     API     │ │   APIs      │           │ │
│  │  │  (Port 5432)│ │  (Port 9000)│ │             │ │             │           │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Clean Architecture (C# Web Application)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Presentation Layer                                 │
│                              (AutoRag.Presentation.Web)                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│  • Blazor Server Pages                                                          │
│  • MudBlazor UI Components                                                      │
│  • ViewModels (MVVM Pattern)                                                    │
│  • JavaScript Interop                                                           │
│  • Authentication & Authorization                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Application Layer                                  │
│                              (AutoRag.Application)                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│  • Services (Business Logic)                                                    │
│  • DTOs (Data Transfer Objects)                                                 │
│  • Interfaces (Contracts)                                                       │
│  • AutoMapper Profiles                                                          │
│  • Dependency Injection                                                         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Domain Layer                                       │
│                              (AutoRag.Domain)                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│  • Entities (User, RagConfig, ChatMessage, etc.)                                │
│  • Repository Interfaces                                                        │
│  • Domain Services                                                              │
│  • Value Objects                                                                │
│  • Domain Events                                                                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Infrastructure Layer                               │
│                              (AutoRag.Infrastructure)                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│  • Entity Framework Core                                                        │
│  • PostgreSQL + pgvector                                                        │
│  • MinIO File Storage                                                           │
│  • External API Clients                                                         │
│  • Repository Implementations                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Микросервисная архитектура

#### 🔍 Document Processor Service
- **Парсинг документов** в различных форматах (PDF, DOCX, XLSX, TXT, изображения)
- **Извлечение текста** с поддержкой OCR для изображений
- **Интеллектуальное разбиение на чанки** с использованием LLM или batch-метода
- **Генерация векторных эмбеддингов** для семантического поиска
- **Обработка таблиц** с сохранением структуры данных

#### 🧠 RAG Service
- **Семантический поиск** по векторным эмбеддингам документов
- **Контекстная генерация** ответов с использованием LLM
- **Настраиваемые промпты** для различных сценариев использования
- **Поддержка чатов** с историей сообщений
- **Фильтрация по релевантности** с настраиваемым порогом

## 🔧 Технологический стек

### Frontend & Web Framework
- **[ASP.NET Core 8.0](https://dotnet.microsoft.com/)** - Современный веб-фреймворк
- **[Blazor Server](https://blazor.net/)** - Интерактивный веб-интерфейс
- **[MudBlazor](https://mudblazor.com/)** - Material Design компоненты
- **[MVVM Pattern](https://docs.microsoft.com/en-us/xamarin/xamarin-forms/enterprise-application-patterns/mvvm)** - Архитектурный паттерн

### Backend & Microservices
- **[FastAPI](https://fastapi.tiangolo.com/)** - Высокопроизводительный Python веб-фреймворк
- **[Python 3.8+](https://www.python.org/)** - Язык программирования для микросервисов
- **[Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)** - Архитектурный паттерн

### Database & Storage
- **[PostgreSQL 16](https://www.postgresql.org/)** - Реляционная база данных
- **[pgvector](https://github.com/pgvector/pgvector)** - Векторные операции
- **[MinIO](https://min.io/)** - Объектное хранилище
- **[Entity Framework Core](https://docs.microsoft.com/en-us/ef/core/)** - ORM для .NET

### AI & Machine Learning
- **[OpenAI GPT-4o-mini](https://openai.com/)** - Языковая модель
- **[Sentence Transformers](https://www.sbert.net/)** - Генерация эмбеддингов
- **[FAISS](https://github.com/facebookresearch/faiss)** - Векторный поиск

### Infrastructure & DevOps
- **[Docker](https://www.docker.com/)** - Контейнеризация
- **[Docker Compose](https://docs.docker.com/compose/)** - Оркестрация сервисов
- **[Health Checks](https://docs.microsoft.com/en-us/aspnet/core/host-and-deploy/health-checks)** - Мониторинг состояния

## 📁 Структура проекта

```
auto-rag/
├── 📁 Web/                          # C# Blazor Web Application
│   ├── 📁 src/
│   │   ├── 📁 Application/          # Application Layer (Clean Architecture)
│   │   │   ├── 📁 DTOs/            # Data Transfer Objects
│   │   │   ├── 📁 Interfaces/      # Service Contracts
│   │   │   ├── 📁 Mappers/         # AutoMapper Profiles
│   │   │   └── 📁 Services/        # Business Logic Services
│   │   ├── 📁 Domain/              # Domain Layer
│   │   │   ├── 📁 Common/          # Base Entities
│   │   │   ├── 📁 Entities/        # Domain Entities
│   │   │   └── 📁 Interfaces/      # Repository Contracts
│   │   ├── 📁 Infrastructure/      # Infrastructure Layer
│   │   │   ├── 📁 External/        # External API Clients
│   │   │   ├── 📁 Persistence/     # Database Context & Configurations
│   │   │   ├── 📁 Repositories/    # Repository Implementations
│   │   │   └── 📁 Storage/         # File Storage Services
│   │   └── 📁 Presentation.Web/    # Presentation Layer
│   │       ├── 📁 Pages/           # Blazor Pages
│   │       ├── 📁 Shared/          # Shared Components
│   │       └── 📁 ViewModels/      # MVVM ViewModels
│   └── AutoRag.sln                 # Visual Studio Solution
├── 📁 document_processor/          # Python Microservice
│   ├── 📁 config/                  # Configuration Files
│   ├── document_pipeline.py        # Document Processing Logic
│   ├── main.py                     # FastAPI Application
│   └── requirements.txt            # Python Dependencies
├── 📁 rag_service/                 # Python Microservice
│   ├── 📁 config/                  # Configuration Files
│   ├── embedding_search.py         # Vector Search Logic
│   ├── main.py                     # FastAPI Application
│   └── requirements.txt            # Python Dependencies
├── 📁 db/                          # Database Initialization
│   └── 📁 init/
│       └── 01-init.sql             # Database Schema
├── docker-compose.yml              # Docker Orchestration
└── README.md                       # Project Documentation
```

## 🚀 Быстрый старт

### Предварительные требования

- **Docker** и **Docker Compose**
- **OpenAI API ключ**
- Минимум **4GB RAM**
- **10GB** свободного места на диске

### 1. Клонирование репозитория

```bash
git clone https://github.com/nbusko/auto-rag.git
cd auto-rag
```

### 2. Настройка переменных окружения

```bash
cp env.example .env
```

Отредактируйте `.env` файл:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.proxyapi.ru/openai/v1

# Embedding Model
EMBEDDER_MODEL=sergeyzh/rubert-mini-frida

# OCR Model
OCR_MODEL=gpt-4o-mini
```

### 3. Запуск всех сервисов

```bash
docker-compose up --build
```

### 4. Проверка работоспособности

```bash
# Проверка веб-приложения
curl http://localhost:8080

# Проверка Document Processor
curl http://localhost:5030/api/v1/health

# Проверка RAG Service
curl http://localhost:5050/api/v1/health

# Проверка базы данных
docker exec auto-rag-db-1 pg_isready -U raguser -d ragdb

# Проверка MinIO
curl http://localhost:9000/minio/health/live
```

### 5. Доступ к приложению

- **Веб-интерфейс**: http://localhost:8080
- **MinIO Console**: http://localhost:9001 (minio/minio123)
- **PostgreSQL**: localhost:15434 (raguser/ragpass)

## ⚙️ Конфигурация

### Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `OPENAI_API_KEY` | Ключ API OpenAI | Обязательно |
| `OPENAI_BASE_URL` | Базовый URL для OpenAI API | `https://api.proxyapi.ru/openai/v1` |
| `EMBEDDER_MODEL` | Модель для генерации эмбеддингов | `sergeyzh/rubert-mini-frida` |
| `OCR_MODEL` | Модель для OCR обработки | `gpt-4o-mini` |

### Настройки веб-приложения

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=db;Port=5432;Database=ragdb;Username=raguser;Password=ragpass"
  },
  "Minio": {
    "Endpoint": "http://minio:9000",
    "AccessKey": "minio",
    "SecretKey": "minio123",
    "Bucket": "autorag"
  },
  "ExternalApis": {
    "RagService": "http://rag_service:5050",
    "DocumentProcessor": "http://document_processor:5030"
  }
}
```

### Настройки микросервисов

#### Document Processor (Port 5030)
- **Методы разбиения**: LLM или Batch
- **Размер батча**: 5-2000 символов
- **Поддерживаемые форматы**: PDF, DOCX, XLSX, TXT, изображения
- **OCR поддержка**: Да

#### RAG Service (Port 5050)
- **Top-K поиск**: Настраиваемое количество результатов
- **Порог релевантности**: 0.0-1.0
- **Температура генерации**: 0.0-1.0
- **Кастомные промпты**: Поддерживаются

## 🔌 API Endpoints

### Document Processor API

```http
# Health Check
GET /api/v1/health

# Process Document
POST /api/v1/process
Content-Type: multipart/form-data

# Get Processing Status
GET /api/v1/status/{task_id}
```

### RAG Service API

```http
# Health Check
GET /api/v1/health

# Generate Answer
POST /api/v1/generate
Content-Type: application/json

# Search Documents
POST /api/v1/search
Content-Type: application/json
```

### Web Application API

```http
# Authentication
POST /api/auth/login
POST /api/auth/register

# Chat
GET /api/chat/history
POST /api/chat/send

# Documents
GET /api/documents
POST /api/documents/upload

# RAG Configuration
GET /api/rag/config
PUT /api/rag/config
```

## 📚 Использование

### 1. Регистрация и аутентификация

1. Откройте http://localhost:8080
2. Зарегистрируйтесь или войдите в систему
3. Создайте RAG-конфигурацию

### 2. Загрузка документов

1. Перейдите на страницу "Documents"
2. Загрузите документы в поддерживаемых форматах
3. Дождитесь завершения обработки

### 3. Настройка RAG

1. Перейдите на страницу "RAG Settings"
2. Настройте параметры:
   - **Top-K**: Количество релевантных фрагментов
   - **Temperature**: Креативность ответов
   - **Threshold**: Порог релевантности
   - **Prompts**: Кастомные промпты

### 4. Использование чата

1. Перейдите на страницу "Chat"
2. Задавайте вопросы на естественном языке
3. Система найдет релевантную информацию и сгенерирует ответ

### 5. Аналитика

1. Перейдите на страницу "Year Data"
2. Просматривайте статистику использования
3. Анализируйте эффективность RAG-системы

## 🧪 Тестирование

### Запуск тестов

```bash
# Тестирование микросервисов
python -m pytest test_document_processor.py
python -m pytest test_service.py

# Тестирование веб-приложения
cd Web
dotnet test
```

### Интеграционные тесты

```bash
# Тестирование полного пайплайна
curl -X POST http://localhost:5030/api/v1/process \
  -F "file=@test_document.pdf"

curl -X POST http://localhost:5050/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"query": "test question"}'
```

## 📊 Мониторинг

### Health Checks

```bash
# Проверка состояния всех сервисов
docker-compose ps

# Логи сервисов
docker-compose logs -f rag_service
docker-compose logs -f document_processor
docker-compose logs -f web
```

### Метрики производительности

- **Время обработки документов**
- **Время генерации ответов**
- **Точность семантического поиска**
- **Использование ресурсов**

## 🤝 Вклад в проект

### Разработка

1. **Fork** репозитория
2. Создайте **feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** изменения (`git commit -m 'Add amazing feature'`)
4. **Push** в branch (`git push origin feature/amazing-feature`)
5. Откройте **Pull Request**

### Архитектурные принципы

- **Clean Architecture** - Разделение слоев
- **SOLID принципы** - Качественный код
- **MVVM Pattern** - Разделение логики и представления
- **Dependency Injection** - Слабая связанность
- **Repository Pattern** - Абстракция доступа к данным

### Стандарты кода

- **C#**: Microsoft C# Coding Conventions
- **Python**: PEP 8
- **SQL**: PostgreSQL naming conventions

---

**AutoRAG** - Интеллектуальная система для обработки документов и генерации ответов на основе контекста.

*Создано с ❤️ используя современные технологии и лучшие практики разработки.*
