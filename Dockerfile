FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей для WeasyPrint и mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libjpeg-dev \
    libpng-dev \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Далее установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаем директорию для загрузки файлов и устанавливаем права
RUN mkdir -p /app/static/uploads && chmod -R 777 /app/static/uploads

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]