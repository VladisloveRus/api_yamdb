#  API для проекта YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. 
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

## Технологии
- Python 3.7
- Django 2.2.19
- djangorestframework 3.12.4

## Установка

Скопируйте репозиторий.
```sh
git clone https://github.com/VladisloveRus/api_yamdb
```
Установите и активируйте виртуальное окружение.
```sh
cd api_yamdb
python -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
```
Установите зависимости, выполните миграции и запустите сервер.

```sh
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```
## Документация и примеры
После запуска сервера Вы можете:  
Посмотреть подробную документацию API:
```sh
http://127.0.0.1:8000/redoc/
```
Импортировать тестовые данные командой:
```sh
python manage.py import_csv
```


## Авторы проекта
- Владислав https://github.com/VladisloveRus
- Андрей https://github.com/and-volkov 
- Филипп https://github.com/caveinfix
