# Image for the labs container: Python plus the lab requirements, built once so a container restart keeps them.
FROM python:3.12.7-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1 DEEPEVAL_TELEMETRY_OPT_OUT=YES
WORKDIR /work
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
