FROM postgres:17-bookworm

RUN apt-get update && \
    apt-get install -y \
        python3 python3-pip python3-venv \
        curl unzip groff less \
        && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AWS_DEFAULT_REGION=ca-central-1 \
    AWS_RESPONSE_CHECKSUM_VALIDATION=when_required \
    AWS_REQUEST_CHECKSUM_CALCULATION=when_required

RUN useradd -m appuser && \
    chown -R appuser:appuser /usr/src/app

COPY requirements.txt .
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
ENV PATH="/opt/venv/bin:$PATH"

COPY --chown=appuser:appuser minio/ ./minio/
COPY --chown=appuser:appuser psql/ ./psql/

USER appuser