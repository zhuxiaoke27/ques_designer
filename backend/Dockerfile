# 使用官方 Python 3.12 镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装构建依赖（用于编译 tiktoken 等包）
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 升级 pip 并安装依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口（Zeabur 会自动设置 PORT 环境变量）
EXPOSE 8080

# 使用 Procfile 中定义的启动命令
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 4 --timeout 120 app:app
