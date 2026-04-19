# 使用官方 Python 运行时作为基础镜像
FROM python:3.10-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Asia/Shanghai

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements 文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY DifyAgent/ ./DifyAgent/
COPY main.py .
COPY finance_Agent_project/ ./finance_Agent_project/
COPY clawer_test/ ./clawer_test/

# 创建日志目录
RUN mkdir -p /app/logs

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# 启动应用
CMD ["python", "-m", "uvicorn", "DifyAgent.server:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
