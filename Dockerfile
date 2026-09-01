FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

COPY --chown=appuser:appgroup app.py .
COPY --chown=appuser:appgroup templates templates
COPY --chown=appuser:appgroup static static

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/ready', timeout=2)"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
