# API YaMDB

##### Проект YaMDb собирает отзывы пользователей на произведения.
API-сервис для библиотеки отзывов и комментариев к фильмам/книгам/музыке.
При аутентификации учитываются разные роли пользователей, реализованы разные права доступа. Регистрация осуществлена по JWT-токену.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
$ git clone https://github.com/cloode/api_yamdb
$ cd api_yamdb
```
Cоздать и активировать виртуальное окружение:

```
$ python3 -m venv venv
$ source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
$ python3 -m pip install --upgrade pip
$ pip install -r requirements.txt
```

Выполнить миграции:

```
$ python3 manage.py migrate
```

Заполнить базу данных:

```
$ python3 manage.py fill_tables
```

Запустить проект:

```
$ python3 manage.py runserver
```

#### Технологии
  
* [Python](https://www.python.org)

* [Django REST framework](https://www.django-rest-framework.org)

#### Авторы

**Егор Котов** - *GitHub* - *[cloode](https://github.com/cloode)*

**Настя Лунегова** - *GitHub* - *[lazy-stuff](https://github.com/lazy-stuff)*

**Георгий Цыбаев** - *GitHub* - *[illager10](https://github.com/illager10)*
