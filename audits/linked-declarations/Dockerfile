FROM ubuntu:24.04@sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git zstd python3 \
    && rm -rf /var/lib/apt/lists/*
COPY group.json prepare.py observe.py /audit/
RUN python3 /audit/prepare.py && rm -rf /root/.cache/mathlib
ENV PATH="/opt/lean/bin:${PATH}"
ENV HOME=/tmp
USER 1000:1000
CMD ["python3", "/audit/observe.py"]
