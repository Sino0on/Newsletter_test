# Используем базовый образ Python
FROM python:3.9

# Установка переменной среды для запуска в режиме "производства"
ENV DJANGO_ENV=production

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей проекта
COPY requirements.txt .

# Установка зависимостей через pip
RUN pip install -r requirements.txt

# Копирование остальных файлов проекта
COPY . .

# Копирование entrypoint.sh в контейнер
COPY entrypoint.sh /app/entrypoint.sh

# Установка разрешений для entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Использование entrypoint.sh в качестве точки входа
ENTRYPOINT ["/app/entrypoint.sh"]


# Запуск команды для создания базы данных и выполнения миграций
RUN python manage.py makemigrations
RUN python manage.py migrate

# Запуск команды для запуска Django приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
