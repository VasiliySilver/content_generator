.PHONY: help build up down logs celery-logs test lint

help:
	@echo "Команды Makefile:"
	@echo "  help          - Показать это сообщение"
	@echo "  build         - Собрать Docker контейнеры"
	@echo "  up            - Запустить все сервисы"
	@echo "  down          - Остановить все сервисы"
	@echo "  logs          - Показать логи всех сервисов"
	@echo "  celery-logs   - Показать логи Celery"
	@echo "  test          - Запустить тесты"
	@echo "  lint          - Проверить код"
RUN ls -la
build:
	docker compose -f docker/docker-compose.yml build

up:
	docker compose -f docker/docker-compose.yml up -d

down:
	docker compose -f docker/docker-compose.yml down

logs:
	docker compose -f docker/docker-compose.yml logs

celery-logs:
	docker compose -f docker/docker-compose.yml logs celery-worker

test:
	pytest

lint:
	flake8 .
