FROM python:3.8

ADD . /neon_metrics_service
WORKDIR /neon_metrics_service
RUN apt-get update && \
    apt-get install -y \
    gcc \
    python3  \
    python3-dev  \
    && pip install wheel  \
    && pip install .

WORKDIR /config

ENV NEON_CONFIG_PATH /config
ENV NEON_METRICS_DIR /metrics

CMD ["neon_metrics_service"]