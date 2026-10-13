FROM ubuntu:24.04@sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git zstd python3 passwd util-linux \
    && rm -rf /var/lib/apt/lists/*
RUN if ! getent passwd 1000 >/dev/null; then useradd --create-home --uid 1000 atlas-observer; fi
COPY group.json prepare.py observe.py /audit/
RUN python3 /audit/prepare.py && rm -rf /tmp/atlas-mathlib-cache
ENV PATH="/opt/lean/bin:${PATH}"
USER 1000:1000
CMD ["python3", "/audit/observe.py"]
