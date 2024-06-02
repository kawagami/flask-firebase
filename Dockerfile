# 使用官方的 Python 映像作為基礎
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 複製當前目錄內容到容器中的 /app 目錄
# COPY . /app
COPY ./app.py /app/app.py
COPY ./requirements.txt /app/requirements.txt

# 安裝所需的 Python 包
RUN pip install --no-cache-dir -r requirements.txt

# 設置環境變量以啟用調試模式
ENV FLASK_ENV=development

# 運行 Flask 應用
CMD ["python", "app.py"]
