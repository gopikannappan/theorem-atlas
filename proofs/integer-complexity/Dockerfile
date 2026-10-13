FROM ubuntu:24.04@sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git zstd \
    && rm -rf /var/lib/apt/lists/*
RUN curl --fail --location --retry 3 \
      https://github.com/leanprover/lean4/releases/download/v4.34.0-rc1/lean-4.34.0-rc1-linux.tar.zst \
      -o /tmp/lean.tar.zst \
    && echo '41dc6a6ec143ece8ed4ba4c4c6978c91f21ad5cbe3c4e7728ad31b869961dc17  /tmp/lean.tar.zst' | sha256sum -c - \
    && mkdir -p /opt/lean \
    && tar --zstd -xf /tmp/lean.tar.zst -C /opt/lean --strip-components=1 \
    && rm /tmp/lean.tar.zst
ENV PATH="/opt/lean/bin:${PATH}"
WORKDIR /work
COPY lean-toolchain lakefile.toml lake-manifest.json ./
# Only pinned upstream code is built here. Candidate code is mounted later.
RUN lake exe cache get && lake build OpenProblemsLab.IntegerComplexity \
    && rm -rf /root/.cache/mathlib \
    && chmod -R a+rX /work /opt/lean
ENV HOME=/tmp
USER 1000:1000
CMD ["lake", "env", "lean", "-DwarningAsError=true", "IntegerComplexity.lean"]
