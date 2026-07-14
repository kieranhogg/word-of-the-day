# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 nonroot \
    && chown nonroot:nonroot /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_TOOL_BIN_DIR=/usr/local/bin
ENV UV_CACHE_DIR=/app/.cache/uv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
COPY --chown=nonroot:nonroot . .
COPY --chown=nonroot:nonroot data/ ./data
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked \
    && mkdir -p /app/.cache/uv \
    && chown -R nonroot:nonroot /app/.cache
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT []
USER nonroot
CMD ["uv", "run", "main.py", "--port", "8080", "--host", "0.0.0.0", "--reload"]
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/docs')" || exit 1