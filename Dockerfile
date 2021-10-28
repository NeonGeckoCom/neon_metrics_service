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

ENV NEON_MQ_PROXY_CONFIG_PATH /config/config.json
ENV NEON_METRICS_DIR /metrics
RUN mkdir ~/.config && \
    ln -s /config ~/.config/neon

CMD ["neon_metrics_service"]