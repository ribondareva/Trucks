FROM python:3.11-slim

# Установим зависимости GDAL, GEOS и PostgreSQL
RUN apt-get update && apt-get install -y \
    binutils \
    gdal-bin \
    libproj-dev \
    libgdal-dev \
    libpq-dev \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установим переменную окружения GDAL, чтобы Django мог найти библиотеку
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Установим зависимости проекта
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Укажем путь к библиотеке GDAL
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

CMD ["gunicorn", "trucks.wsgi:application", "--bind", "0.0.0.0:8000"]
