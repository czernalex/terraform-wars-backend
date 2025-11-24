.PHONY: run
run:
	uv run manage.py runserver 8080

.PHONY: migrate
migrate:
	uv run manage.py migrate

.PHONY: shell
shell:
	uv run manage.py shell

.PHONY: test
test:
	uv run pytest --reuse-db  --cov=main --cov-report=html

.PHONY: lint
lint:
	uv run pre-commit run --all-files

.PHONY: activate-venv
activate-venv:
	source .venv/bin/activate
