# 使用国内 DaoCloud 镜像源，绕过官方 Docker Hub 屏蔽
ARG BASE_IMAGE=docker.m.daocloud.io/library/python:3.11-slim-bookworm

# ================================
# 第一阶段：构建依赖 (Builder)
# ================================
FROM ${BASE_IMAGE} AS builder

WORKDIR /app

# 更换中科大源
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources

# 安装构建必需的系统包
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        build-essential \
        libjpeg-dev \
        libpng-dev \
        libfreetype6-dev \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# 创建Python虚拟环境
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装Playwright及其浏览器（利用pip安装playwright后下载chromium）
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN playwright install chromium

# ================================
# 第二阶段：最终运行环境 (Runner)
# ================================
FROM ${BASE_IMAGE}

# 设置标签信息
LABEL maintainer="zhinianboke"
LABEL version="2.1.0"
LABEL description="闲鱼自动回复系统 - 企业级多用户版本，支持自动发货和免拼发货"
LABEL repository="https://github.com/zhinianboke/xianyu-auto-reply"
LABEL license="仅供学习使用，禁止商业用途"
LABEL author="zhinianboke"

WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TZ=Asia/Shanghai
ENV DOCKER_ENV=true
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PATH="/opt/venv/bin:$PATH"

# 更换中科大源
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources

# 安装必要的运行时系统依赖 (去除冗余的 npm, chromium 等)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nodejs \
        tzdata \
        curl \
        ca-certificates \
        fonts-dejavu-core \
        fonts-liberation \
        libnss3 \
        libnspr4 \
        libatk-bridge2.0-0 \
        libdrm2 \
        libxkbcommon0 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        libgbm1 \
        libxss1 \
        libasound2 \
        libatspi2.0-0 \
        libgtk-3-0 \
        libgdk-pixbuf2.0-0 \
        libxcursor1 \
        libxi6 \
        libxrender1 \
        libxext6 \
        libx11-6 \
        libxft2 \
        libxinerama1 \
        libxtst6 \
        libappindicator3-1 \
        libx11-xcb1 \
        libxfixes3 \
        xdg-utils \
        xvfb \
        x11vnc \
        fluxbox \
        libgl1 \
        libglib2.0-0 \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && rm -rf /tmp/* \
        && rm -rf /var/tmp/*

# 设置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 验证Node.js安装
RUN node --version

# 从builder阶段复制虚拟环境和Playwright浏览器缓存
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /ms-playwright /ms-playwright

# 安装Playwright所需的浏览器系统依赖
RUN playwright install-deps chromium

# 复制项目文件
COPY . .

# 创建必要的目录并设置权限
RUN mkdir -p /app/logs /app/data /app/backups /app/static/uploads/images && \
    chmod 777 /app/logs /app/data /app/backups /app/static/uploads /app/static/uploads/images

# 配置系统限制，防止core文件生成
RUN echo "ulimit -c 0" >> /etc/profile

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
