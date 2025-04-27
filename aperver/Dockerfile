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

# コンテナ内で公開するポート
EXPOSE 5000

# 環境変数の設定
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# アプリケーションの実行
CMD ["flask", "run"]
