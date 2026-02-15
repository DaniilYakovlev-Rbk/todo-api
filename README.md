# Todo API — REST API для управления задачами

Простое REST API для ведения списка задач (To-Do List).  

## Стек технологий

- **Язык**: Python 3.11
- **Фреймворк**: FastAPI
- **База данных**: PostgreSQL + SQLAlchemy
- **Контейнеризация**: Docker + docker-compose
- **Документация API**: Swagger UI / ReDoc (автогенерация)

## Основной функционал

- Создание новой задачи (`POST /tasks/`)
- Получение списка всех задач (`GET /tasks/`)
- Фильтрация по статусу: все / завершённые / активные (`?completed=true/false`)
- Получение задачи по ID (`GET /tasks/{task_id}`)
- Изменение статуса задачи (завершить / возобновить) (`PATCH /tasks/{task_id}`)
- Удаление задачи (`DELETE /tasks/{task_id}`)

## Запуск 

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/todo-api.git
cd todo-api
```

### 2. Настройте переменные окружения

Скопируйте пример .env.example в .env и отредактируйте под себя 

### 3. Запустите контейнеры

```bash
docker-compose up --build
```

После успешного запуска API будет доступно по адресу:
http://localhost:8000

Документация Swagger: http://localhost:8000/docs

##  Проверка работы

### Через браузер (Swagger UI)

Откройте http://localhost:8000/docs — вы увидите интерактивную документацию, где можно выполнять все запросы прямо из браузера.

###  Через curl

- Создать задачу
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Купить молоко", "description": "Обязательно безлактозное"}'
```

- Получить все задачи
```bash
curl "http://localhost:8000/tasks/"
```

- Получить только активные задачи
```bash
curl "http://localhost:8000/tasks/?completed=false"
```

- Получить только выполненные
```bash
curl "http://localhost:8000/tasks/?completed=true"
```

- Получить задачу по ID
```bash
curl "http://localhost:8000/tasks/ВАШ_ID"
```

- Изменить статус задачи (выполнена)
```bash
curl -X PATCH "http://localhost:8000/tasks/ВАШ_ID" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

- Удалить задачу
```bash
curl -X DELETE "http://localhost:8000/tasks/ВАШ_ID"
```

# Контакты

Буду рад обратной связи, я всегда готов обсудить детали и ответить на ваши вопросы при необходимости:

* Email: yakovlevprogrammer.@gmail.com

* Telegram: @YakovlevProgrammer
