FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    ORDERFLOW_ENVIRONMENT=production

WORKDIR /app

RUN groupadd --system orderflow && useradd --system --gid orderflow --create-home orderflow \
    && mkdir -p /app/data/runtime \
    && chown -R orderflow:orderflow /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src
ENV PYTHONPATH=/app/src
RUN chown -R orderflow:orderflow /app

USER orderflow
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

CMD ["python", "-m", "uvicorn", "orderflow.main:app", "--host", "0.0.0.0", "--port", "8000"]
