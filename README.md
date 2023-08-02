<!-- PROJECT LOGO -->
<div align="center">
  <h2>BBoom-test</h2>

  <h3 align="center">README тестового задания</h3>

  <p align="center">
    Веб-приложение на Django, для взаимодействия объектов пользователей и постов
  </p>
</div>

<a name="readme-top"></a>

<hr>

<!-- ABOUT THE PROJECT -->
## About The Project

Задачи:
* Создание моделей данных: Создайте две модели данных: User и Post. Модель User должна содержать следующие поля: id (
уникальный идентификатор), name (имя пользователя), email (электронная почта пользователя). Модель Post должна содержать
следующие поля: id (уникальный идентификатор), user (ссылка на пользователя, который создал пост), title (заголовок
поста), body (текст поста).

* Создание API: Создайте несколько API-конечных пунктов. Первый должен возвращать список всех пользователей, второй -
список всех постов конкретного пользователя, третий - добавление нового поста, четвертый - удаление существующего поста.

* Аутентификация и авторизация: Реализуйте механизм аутентификации и авторизации. Только аутентифицированные пользователи
могут добавлять и удалять посты. Пользователи могут удалять только свои посты.

* Тестирование API: Напишите unit-тесты для проверки корректности работы вашего API, включая тесты аутентификации и
авторизации.

* Создание пользовательского интерфейса: Создайте пользовательский интерфейс с использованием Django templates, который
будет отображать список всех пользователей. При клике на имя пользователя, должен открываться список его постов.
Добавьте формы для добавления и удаления постов.


Требования::
* Проект должен быть создан с использованием Django и Python.
* Для создания API используйте Django REST Framework.
* Для тестирования API используйте Django Test Client или pytest.
* Все данные должны быть сохранены в базе данных SQLite.
* Код должен быть размещен на GitHub или Bitbucket и должен включать инструкции по установке и запуску приложения.

### Built With

* [![Django][Django-badge]][Django-url]
* [![SQLite][SQLite-badge]][SQLite-url]
* [![Docker][Docker-badge]][Docker-url]

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Copy project to repository on local machine (HTTPS or SSH)
  ```sh
  git clone https://github.com/SuperLalka/BBoom-test.git
  ```
  ```sh
  git clone git@github.com:SuperLalka/BBoom-test.git
  ```

### Installation

To start the project, it is enough to build and run docker containers.
Database migration and fixture loading will be applied automatically.

1. Build docker containers
   ```sh
   docker-compose -f docker-compose.yml build
   ```
2. Run docker containers
   ```sh
   docker-compose -f docker-compose.yml up -d
   ```

### Documentation

The project API documentation is located at

    http://0.0.0.0:8000/redoc/

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Django-badge]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://docs.djangoproject.com/
[SQLite-badge]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://www.sqlite.org/
[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
