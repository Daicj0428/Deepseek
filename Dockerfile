
FROM python:3.9-slim

WORKDIR /app

# 先复制requirements.txt
COPY scripts/requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制其余文件
COPY . .

# 暴露端口
EXPOSE 21048

# 设置环境变量
ENV FLASK_APP=scripts/app.py
ENV FLASK_DEBUG=0
ENV DEEPSEEK_API_URL=https://api.deepseek.com/
ENV DEEPSEEK_MODEL=deepseek-chat
ENV FLASK_SECRET=dev-secret-key
ENV PROT=21048
ENV TZ=Asia/Shanghai


# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:21048", "--worker-class", "eventlet", "-w", "1", "scripts.app:app"]
