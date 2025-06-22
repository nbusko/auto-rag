.PHONY: help build up down logs test clean restart

# Переменные
COMPOSE_FILE = docker-compose.yml
SERVICES = postgres data_service rag_service

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Собрать образы Docker
	docker-compose -f $(COMPOSE_FILE) build

up: ## Запустить все сервисы
	docker-compose -f $(COMPOSE_FILE) up -d

down: ## Остановить все сервисы
	docker-compose -f $(COMPOSE_FILE) down

restart: ## Перезапустить все сервисы
	docker-compose -f $(COMPOSE_FILE) restart

logs: ## Показать логи всех сервисов
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-data: ## Показать логи Data Service
	docker-compose -f $(COMPOSE_FILE) logs -f data_service

logs-rag: ## Показать логи RAG Service
	docker-compose -f $(COMPOSE_FILE) logs -f rag_service

logs-postgres: ## Показать логи PostgreSQL
	docker-compose -f $(COMPOSE_FILE) logs -f postgres

test: ## Запустить тесты системы
	python test_services.py

test-old: ## Запустить старые тесты системы
	python test_system.py

clean: ## Очистить все контейнеры и образы
	docker-compose -f $(COMPOSE_FILE) down -v --rmi all
	docker system prune -f

status: ## Показать статус сервисов
	docker-compose -f $(COMPOSE_FILE) ps

health: ## Проверить здоровье сервисов
	@echo "Проверка Data Service..."
	@curl -s http://localhost:5050/health || echo "Data Service недоступен"
	@echo "Проверка RAG Service..."
	@curl -s http://localhost:5060/health || echo "RAG Service недоступен"

swagger: ## Открыть Swagger UI в браузере
	@echo "Открытие Swagger UI..."
	@echo "Data Service: http://localhost:5050/docs"
	@echo "RAG Service: http://localhost:5060/docs"
	@if command -v xdg-open > /dev/null; then \
		xdg-open http://localhost:5050/docs; \
		xdg-open http://localhost:5060/docs; \
	elif command -v open > /dev/null; then \
		open http://localhost:5050/docs; \
		open http://localhost:5060/docs; \
	else \
		echo "Откройте в браузере:"; \
		echo "  Data Service: http://localhost:5050/docs"; \
		echo "  RAG Service: http://localhost:5060/docs"; \
	fi

setup: ## Первоначальная настройка системы
	@echo "Настройка AutoRAG системы..."
	@if [ ! -f .env ]; then \
		echo "Создание .env файла из примера..."; \
		cp env.example .env; \
		echo "⚠️  Не забудьте настроить OPENAI_API_KEY в .env файле!"; \
	fi
	@echo "Сборка и запуск сервисов..."
	$(MAKE) build
	$(MAKE) up
	@echo "Ожидание готовности сервисов..."
	@sleep 30
	@echo "Проверка здоровья сервисов..."
	$(MAKE) health

dev: ## Запуск для разработки (только PostgreSQL)
	docker-compose -f $(COMPOSE_FILE) up postgres -d
	@echo "PostgreSQL запущен. Запустите сервисы локально:"
	@echo "cd data_service && pip install -r requirements.txt && python main.py"
	@echo "cd rag_service && pip install -r requirements.txt && python main.py"

debug: ## Запуск с выводом логов
	docker-compose -f $(COMPOSE_FILE) up

rebuild: ## Пересобрать и перезапустить сервисы
	$(MAKE) down
	$(MAKE) build
	$(MAKE) up
	@echo "Сервисы пересобраны и запущены"
	@echo "Ожидание готовности..."
	@sleep 10
	$(MAKE) health 