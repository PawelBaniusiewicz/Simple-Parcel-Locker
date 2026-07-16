FROM python:3.14
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFERED 1
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /webapp
COPY pyproject.toml uv.lock ./
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"
RUN uv sync --frozen
ENV PATH="/opt/venv/bin:$PATH"
COPY . /webapp/
COPY .env /webapp/