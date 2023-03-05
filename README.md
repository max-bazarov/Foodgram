# Foodgram

http://digital-foodgram.sytes.net/

[![Backend workflow](https://github.com/max-bazarov/foodgram-project-react/actions/workflows/backend_workflow.yml/badge.svg)](https://github.com/max-bazarov/foodgram-project-react/actions/workflows/backend_workflow.yml)

## Описание
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологии
- Python 3.10.4
- Django REST Framework
- PostgreSQL
- Docker
- Nginx
- Gunicorn

## Установка и локальный запуск
- Склонируйте репозиторий на свой компьютер
- Измените файл .env.dist на .env и заполните его
- Убедитесь, что у вас установлен Docker и Docker Compose последних версий
- Запустите проект командой `docker-compose up`
- При первом запуске проекта необходимо выполнить миграции командой `docker-compose exec web python manage.py migrate`
- Создайте суперпользователя командой `docker-compose exec web python manage.py createsuperuser`
- Проект доступен по адресу http://localhost/ 

## Пример запросов
Примеры запросов можно увидеть в документации

http://digital-foodgram.sytes.net/api/docs/