#!/bin/bash

# Создание базы данных
psql -U postgres -c "CREATE DATABASE mydatabase2;"

# Выполнение миграций для основной базы данных
python manage.py migrate

# Запуск Django приложения
exec "$@"
