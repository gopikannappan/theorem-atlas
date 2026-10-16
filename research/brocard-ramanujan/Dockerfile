FROM ubuntu:24.04@sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl zstd python3 python3-venv && rm -rf /var/lib/apt/lists/*
RUN curl --fail --location --connect-timeout 20 --max-time 240 --retry 2 https://github.com/leanprover/lean4/releases/download/v4.34.1/lean-4.34.1-linux.tar.zst -o /tmp/lean.tar.zst \
    && echo "47bf4bbd78f70c2e9670598ab7124d92b6efb7330ff33e5fbb4030f6fd72e4e4  /tmp/lean.tar.zst" | sha256sum -c - \
    && mkdir /opt/lean && tar --zstd -xf /tmp/lean.tar.zst -C /opt/lean --strip-components=1 && rm /tmp/lean.tar.zst
RUN python3 -m venv /opt/research && /opt/research/bin/pip install --no-cache-dir sympy==1.14.0 mpmath==1.3.0
COPY . /research
ENV PATH="/opt/lean/bin:/opt/research/bin:$PATH"
WORKDIR /tmp
USER 65534:65534
