install:
	uv sync --all-groups
fmt:
	uv run ruff format .
lint:
	uv run ruff check .
