FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV VIRTUAL_ENV=/home/ubuntu/.local/venv

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    ca-certificates \
    cmake \
    curl \
    gdb \
    git \
    gnupg \
    lsb-release \
    make \
    ninja-build \
    nodejs \
    npm \
    openssh-client \
    pkg-config \
    python3 \
    python3-pip \
    python3-venv \
    ripgrep \
    software-properties-common \
    sudo \
    tmux \
    unzip \
    vim \
    wget \
    zip \
    zlib1g-dev \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

RUN LLVM_VERSION=23 \
    && wget -qO /tmp/llvm.sh https://apt.llvm.org/llvm.sh \
    && chmod +x /tmp/llvm.sh \
    && /tmp/llvm.sh "${LLVM_VERSION}" all \
    && rm -f /tmp/llvm.sh \
    && for tool in clang clang++ clangd clang-format clang-tidy lld lldb llvm-config; do \
           if [ -x "/usr/bin/${tool}-${LLVM_VERSION}" ]; then \
               update-alternatives --install "/usr/bin/${tool}" "${tool}" "/usr/bin/${tool}-${LLVM_VERSION}" 100; \
           fi; \
       done \
    && rm -rf /var/lib/apt/lists/*

RUN if id -u ubuntu >/dev/null 2>&1; then \
        usermod -s /bin/bash -aG sudo ubuntu; \
    else \
        useradd -ms /bin/bash -G sudo ubuntu; \
    fi \
    && echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu

RUN npm install -g @openai/codex

USER ubuntu

RUN python3 -m venv "${VIRTUAL_ENV}" \
    && "${VIRTUAL_ENV}/bin/pip" install --no-cache-dir --upgrade pip setuptools wheel \
    && "${VIRTUAL_ENV}/bin/pip" install --no-cache-dir \
        anthropic \
        claude-code-sdk \
        ipython \
        openai \
        openai-agents \
        pydantic \
        pydantic-settings \
        pytest \
        python-dotenv \
        requests \
        rich \
        ruff \
        typer \
        uv

ENV USER=ubuntu
ENV HOME=/home/ubuntu
ENV CARGO_HOME=/home/ubuntu/.cargo
ENV RUSTUP_HOME=/home/ubuntu/.rustup
ENV PATH=/home/ubuntu/.cargo/bin:/home/ubuntu/.local/venv/bin:${PATH}

RUN curl -fsSL https://claude.ai/install.sh | bash

RUN curl -L code.kimi.com/install.sh | bash

RUN curl https://sh.rustup.rs -sSf | bash -s -- -y --profile default --default-toolchain stable \
    && rustup component add clippy rustfmt

WORKDIR /workspaces
