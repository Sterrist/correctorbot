FROM python:3.12-slim AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN groupadd --system appgroup \
    && useradd --system --gid appgroup appuser

COPY --from=builder --chown=appuser:appgroup /app /app

RUN /app/.venv/bin/python -c \
    "import aiogram, openai; print('aiogram:', aiogram.__version__)"

USER appuser

CMD ["/app/.venv/bin/python", "run.py"]
