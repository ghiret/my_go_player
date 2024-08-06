FROM python:3.12

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y gnupg && \
    apt-key update && \
    apt-get update --allow-insecure-repositories && \
    apt-get install -y --allow-unauthenticated \
    sudo \
    git \
    curl \
    zsh \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m devuser && \
    echo "devuser ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/devuser && \
    chmod 0440 /etc/sudoers.d/devuser

RUN mkdir /workspace && chown devuser:devuser /workspace

USER devuser
WORKDIR /home/devuser

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

RUN sudo chsh -s $(which zsh) devuser

# Update pip and install Python development tools
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    pre-commit \
    black \
    flake8 \
    isort \
    mypy \
    pylint \
    pytest \
    coverage \
    poetry


WORKDIR /workspace

SHELL ["/bin/zsh", "-c"]

# Add /workspace as a safe directory for Git
RUN git config --global --add safe.directory /workspace
