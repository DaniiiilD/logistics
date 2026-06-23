run:
	uv run uvicorn src.main:app --reload

	uv run python -m uvicorn src.main:app --reload

migrate:
	uv run alembic revision --autogenerate -m 'auto'

upgrade:
	uv run alembic upgrade head

ruff:
	uv run ruff format .
	uv run ruff check . --fix

grpc: 
	uv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. src/api/grpc/tariff.proto

docker:
	docker-compose up -d

celery: 
	uv run celery -A src.api.services.celery.celery_app worker --loglevel=info -P solo

mcp:
	npx @modelcontextprotocol/inspector uv run mcp-start
	$env:PYTHONPATH="."; npx @modelcontextprotocol/inspector uv run mcp-start

test:
	uv run pytest --cov=src
	uv run pytest
	uv run pytest --cov=src --cov-report=html
	Start-Process htmlcov/index.html

html:
	uv run python -m http.server 8080
