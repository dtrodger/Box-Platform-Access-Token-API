# Makefile

help:
	@echo
	@echo "  Box Platform access token API Makefile"
	@echo "  -----------------------------------------------------------------------------------------------------------"
	@echo "  dev                       to build the development Docker images"

dev:
	docker-compose -f docker-compose.dev.yml down
	docker-compose -f docker-compose.dev.yml up
