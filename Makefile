run:
	uv run uvicorn src.main:app --reload

migrate:
	uv run alembic revision --autogenerate -m 'auto'

upgrade:
	uv run alembic upgrade head

ruff:
	uv run ruff format .
	uv run ruff check . --fix