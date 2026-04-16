# Meeting Master

**API для бронирования переговорных комнат**

---

## 📌 О проекте

`Meeting Master` предоставляет REST API для управления переговорными комнатами. Пользователи могут регистрироваться, входить в систему (авторизация через токены в cookies), просматривать список комнат, а также создавать и удалять их (последние два действия — только для авторизованных пользователей).

Проект написан на **FastAPI** с использованием **PostgreSQL** в качестве основной базы данных (через Docker) и полностью контейнеризирован для удобного развертывания.

---

## 🚀 Возможности

- **Регистрация и аутентификация пользователей** через cookies.
- **Просмотр списка всех комнат** (доступен всем).
- **Создание и удаление комнат** (только для авторизованных пользователей).
- **PostgreSQL** в Docker для надежного хранения данных.
- **Токены доступа с ограниченным временем жизни**.
- **Готов к развертыванию** с помощью Docker Compose.

---

## 🛠️ Технологии

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-100000?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=uvicorn&logoColor=white)
![UV](https://img.shields.io/badge/UV-4B32C3?style=for-the-badge&logo=uv&logoColor=white)

---

## 🖥️ Запуск через Docker

1. Клонируй репозиторий:
   ```bash
   git clone https://github.com/imnokkip/Meeting-Master
   cd Meeting-Master
   ```

2. Скопируй и настрой переменные окружения:
   ```bash
   cp .env.example .env
   Отредактируй .env при необходимости
   ```

3. Запусти Docker:
   ```bash
   docker-compose up -d
   ```

4. Открой в браузере `http://127.0.0.1:8000/docs` для доступа к Swagger-документации.

---

## 📑 Планы по доработке

Этот проект — не финальная точка, а рабочий прототип, который я буду улучшать. В ближайшее время планирую:

- [ ] **Реализовать систему прав пользователей.** Сейчас любой авторизованный пользователь может создать или удалить комнату. Нужно добавить роли (`admin`, `user`), чтобы управление комнатами было доступно только администраторам.
- [ ] **Добавить возможность бронирования комнат.** Пользователи должны иметь возможность забронировать комнату на определенное время с проверкой конфликтов (нельзя забронировать уже занятую комнату).
- [ ] **Исправить вывод данных.** Сейчас эндпоинты возвращают объекты SQLAlchemy, что неоптимально. Нужно настроить Pydantic-схемы для ответов (response_model).
- [ ] **Нормализовать статусы ответов и ошибки.** Вместо `return False` использовать понятные исключения `HTTPException` с корректными кодами (401, 403, 404, 409).
- [ ] **Улучшить архитектуру:** разделить `database.py` на модули (`crud_rooms.py`, `crud_users.py`, `auth.py`), чтобы код стал чище и проще в поддержке.

---
