# shell - оболочка, /bin/bash - путь к запуску
SHELL := /bin/bash

# область видимости
all: run_uvcorn


# .PHONY: - ключевое слово команды, requirements - название команды
.PHONY: requirements
# requirements: - название команды, pyproject.toml - ссылка на то что нужно запустить
requirements: pyproject.toml
	poetry lock
	poetry install --no-root


.PHONY: migration-generate
migration-generate: requirements
	poetry run alembic revision --autogenerate -m "Initial revision"

.PHONY: migration-upgrade
migration-upgrade: requirements
	poetry run alembic upgrade head


.PHONY: run_uvicorn
run_uvicorn: requirements migration-upgrade
	poetry run uvicorn src.main:app --reload