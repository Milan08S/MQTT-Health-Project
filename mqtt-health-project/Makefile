COMPOSE_FILE := docker-compose.yml

down:
	docker-compose -f $(COMPOSE_FILE) down

clean-db: down
	docker volume rm mqtt-health-project_pgdata

up: 
	docker-compose -f $(COMPOSE_FILE) up -d

.PHONY: up down clean-db