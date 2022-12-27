# API_YAMDB 
[![yamdb_workflow](https://github.com/mrblessk/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/mrblessk/yamdb_final/actions/workflows/yamdb_workflow.yml)


### Описание
Проект собирает отзывы (Review) пользователей на произведения (Titles).
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). 
На одно произведение пользователь может оставить только один отзыв.

### **Стек**

![python version](https://img.shields.io/badge/Python-3.7.9-green)
![django version](https://img.shields.io/badge/Django-2.2.16-green)
![django-rest-framework](https://img.shields.io/badge/django_rest_framework-3.12.4-green)
![nginx version](https://img.shields.io/badge/Nginx-1.21.3-green)
![docker version](https://img.shields.io/badge/Docker-4.15-green)
![gunicorn version](https://img.shields.io/badge/Gunicorn-20.0.4-green)


### Как запустить проект:

Клонируйте репозиторий и перейдите в директорию для развертывания инфраструктуры в командной строке:

```
git clone https://github.com/mrblessk/infra_sp2.git
```

```
cd infra
```

Заполните файл "/infra/.env.dist/.env.sample" по примеру, переместите его в каталог "infra/" и переименуйте в ".env":
```
DB_NAME = postgres
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
DB_HOST = db
DB_PORT = 5432
SECRET_KEY = key
DEBUG = True/False
ALLOWED_HOSTS = ['hosts']
```

Разверните контейнер:
```
sudo docker-compose up
```

Выполните миграции, создайте профиль администратора и выполните команду для сбора статики:
```
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
```

После проект будет доступен по адресу http://localhost/


### Примеры использования api:
Получение произведений:
```
GET /api/v1/titles/
```
Добавление произведения (только администратор):
```
POST /api/v1/titles/
```
В параметрах передавать json:
```
{
    "name": "Название произведения",
    "year": 1900,
    "description": "Описание произведения",
    "genre": [
    "Жанр",
    ],
    "category": "Кино"
}
```

Авторы проекта:
```
* Гельруд Борис (https://github.com/Izrekatel/)
* Горелов Дмитрий (https://github.com/Pash1et)
* Сулейманов Роман (https://github.com/mrblessk)

```
