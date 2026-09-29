FROM apache/airflow:2.9.3-python3.11

USER airflow

COPY beam-pipeline/requirements.txt /opt/beam-pipeline/requirements.txt

RUN pip install --no-cache-dir -r /opt/beam-pipeline/requirements.txt

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER root
