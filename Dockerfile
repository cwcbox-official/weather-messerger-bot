# 使用官方 Python 3.10 映像
FROM python:3.10-slim

# 安裝必要套件（包括 ca-certificates）
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製所有程式碼到容器內
COPY . .

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 設定環境變數（可選）
ENV PORT=10000

# 對外開放埠（Render 預設使用 $PORT）
EXPOSE 10000

# 啟動應用程式
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]