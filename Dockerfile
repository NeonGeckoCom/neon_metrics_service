FROM python:3.10-slim

ENV XDG_CONFIG_HOME /config
COPY docker_overlay/ /

RUN apt-get update && \
    apt-get install -y \
    gcc \
    python3  \
    python3-dev  \
    && pip install wheel

ADD . /neon_api_proxy
WORKDIR /neon_api_proxy
RUN pip install .

CMD ["neon_metrics_service"]