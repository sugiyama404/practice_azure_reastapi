# ベースイメージとしてPython 3.11を使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストールするためのファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
