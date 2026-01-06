FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# poetryインストール
RUN pip install poetry

# Poetry の仮想環境を無効化
RUN poetry config virtualenvs.create false

# 依存関係ファイルをコピー
COPY pyproject.toml poetry.lock ./

# install のあと
RUN poetry install --no-root

# あとでアプリケーションソースをコピー（変更が多いため）
COPY . .

# 変更後
# CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT}"]
