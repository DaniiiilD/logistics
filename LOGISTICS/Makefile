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