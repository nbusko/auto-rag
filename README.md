<div id="top"></div>
<h1 align="center">AutoRAG</h1>
<h3 align="center">Platform for NoCode/Auto RAG creating</h3>
</div>

## Архитектура

Система состоит из трех основных компонентов:

- **PostgreSQL** - база данных с расширением pgvector для векторного поиска
- **Data Service** - сервис для управления данными, эмбеддингами и историей чатов
- **RAG Service** - сервис для обработки RAG запросов и генерации ответов
...
**TODO**

## Быстрый старт

### 1. Настройка окружения

```bash
# Клонируйте репозиторий
git clone https://github.com/nbusko/auto-rag.git
cd auto-rag

# Создайте .env файл из примера
cp env.example .env

# Настройте OPENAI_API_KEY в .env файле
# OPENAI_API_KEY=your_api_key_here
```

### 2. Запуск системы

```bash
# Первоначальная настройка и запуск
make setup

# Или пошагово:
make build    # Собрать образы
make up       # Запустить сервисы
```

### 3. Проверка работы

```bash
# Проверить статус сервисов
make status

# Проверить здоровье сервисов
make health

# Открыть Swagger UI
make swagger
```

## Доступные команды

```bash
make help          # Показать все доступные команды
make build         # Собрать Docker образы
make up            # Запустить сервисы
make down          # Остановить сервисы
make restart       # Перезапустить сервисы
make logs          # Показать логи всех сервисов
make logs-data     # Логи Data Service
make logs-rag      # Логи RAG Service
make test          # Запустить тесты
make health        # Проверить здоровье сервисов
make swagger       # Открыть Swagger UI
make rebuild       # Пересобрать и перезапустить
```

## API Endpoints

### Data Service (http://localhost:5050)

- `GET /` - Информация о сервисе
- `GET /health` - Проверка здоровья
- `GET /docs` - Swagger UI
- `GET /chat/{chat_id}` - Получить данные чата
- `POST /chat/{chat_id}/message` - Добавить сообщение
- `POST /chat/{chat_id}/params` - Обновить параметры чата
- `POST /docs/update` - Обновить документы
- `GET /docs/{document_id}/search` - Поиск в документах

### RAG Service (http://localhost:5060)

- `GET /` - Информация о сервисе
- `GET /health` - Проверка здоровья
- `GET /docs` - Swagger UI
- `POST /rag/process` - Обработать RAG запрос
- `GET /chat/{chat_id}/history` - История чата
- `GET /chat/{chat_id}/params` - Параметры чата

## Логирование

Все сервисы настроены с подробным логированием:

- Логи выводятся в консоль и в файлы:
  - `data_service.log` - логи Data Service
  - `rag_service.log` - логи RAG Service

- Уровни логирования:
  - INFO - основная информация о работе
  - ERROR - ошибки и исключения
  - WARNING - предупреждения

## Тестирование

```bash
# Запустить полное тестирование
make test

# Проверить только доступность сервисов
make health
```

## Разработка

### Локальная разработка

```bash
# Запустить только PostgreSQL
make dev

# Запустить сервисы локально
cd data_service && python main.py
cd rag_service && python main.py
```

### Структура проекта

```
auto-rag/
├── data_service/          # Сервис данных
│   ├── main.py           # Основной файл
│   ├── database.py       # Работа с БД
│   ├── embedding_service.py # Эмбеддинги
│   ├── models.py         # Pydantic модели
│   └── requirements.txt  # Зависимости
├── rag_service/          # RAG сервис
│   ├── main.py           # Основной файл
│   ├── database.py       # Работа с БД
│   ├── rag_pipeline.py   # RAG пайплайн
│   ├── models.py         # Pydantic модели
│   └── requirements.txt  # Зависимости
├── docker-compose.yml    # Конфигурация Docker
├── Makefile             # Команды управления
├── test_services.py     # Тесты
└── README.md           # Документация
```

## Требования

- Docker и Docker Compose
- Python 3.11+ (для локальной разработки)
- OpenAI ProxyAPI ключ
