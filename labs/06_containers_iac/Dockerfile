# Lab 06 — a Dockerfile a security reviewer will accept.
# Build:  docker build -t decision-service:1.0.1 .      Run: docker run -p 8080:8080 decision-service:1.0.1
# Pinned base image, non-root user, no secrets in layers, health check, nothing but the app in the final image.
FROM python:3.12.7-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 app
WORKDIR /app
COPY --chown=app:app app.py .
USER app

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2)"
CMD ["python", "app.py"]
