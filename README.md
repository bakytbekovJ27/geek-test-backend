Конечно ✅ Вот готовый аккуратно оформленный **`README.md`** файл для твоего проекта **Django REST Todo List**.
Ты можешь просто создать в корне проекта файл `README.md` и вставить туда этот текст👇

---

# 📝 Django REST Todo List

Простое REST API приложение для управления задачами (**Todo list**) на основе **Django** и **Django REST Framework**.

---

## 🔧 Шаг 1: Подготовка окружения

### 1.1 Проверьте Python

```bash
python --version
# Должна быть версия Python 3.8 или выше
```

### 1.2 Создайте виртуальное окружение (рекомендуется)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 1.3 Установите зависимости

```bash
pip install django djangorestframework
```

---

## 📁 Шаг 2: Создание проекта

### 2.1 Создайте Django проект

```bash
django-admin startproject todoproject
cd todoproject
```

### 2.2 Создайте приложение `tasks`

```bash
python manage.py startapp tasks
```

### 2.3 Структура проекта

```
todoproject/
├── manage.py
├── todoproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── tasks/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── views.py
    └── migrations/
```

---

## ⚙️ Шаг 3: Настройка проекта

### 3.1 Добавьте приложения в `todoproject/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Добавляем эти строки
    'rest_framework',
    'tasks',
]
```

### 3.2 (Опционально) Настройки REST Framework

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

---

## 📝 Шаг 4: Создание файлов приложения

### 4.1 Модель `tasks/models.py`

```python
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
```

### 4.2 Сериализатор `tasks/serializers.py`

```python
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created']
        read_only_fields = ['id', 'created']
```

### 4.3 Views `tasks/views.py`

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

@api_view(['GET', 'POST'])
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Задача не найдена'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Задача успешно удалена'}, status=status.HTTP_204_NO_CONTENT)
```

### 4.4 URLs `tasks/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),
]
```

### 4.5 Основной файл URL `todoproject/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
]
```

### 4.6 (Опционально) Админ панель `tasks/admin.py`

```python
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'completed', 'created']
    list_filter = ['completed', 'created']
    search_fields = ['title', 'description']
```

---

## 🗄️ Шаг 5: Миграции базы данных

```bash
python manage.py makemigrations
python manage.py migrate
```

(опционально) создать суперпользователя:

```bash
python manage.py createsuperuser
```

---

## 🚀 Шаг 6: Запуск сервера

```bash
python manage.py runserver
```

Сервер запустится по адресу:

* API: [http://127.0.0.1:8000/api/tasks/](http://127.0.0.1:8000/api/tasks/)
* Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Шаг 7: Тестирование в Postman

### ✅ 1. Получить все задачи

**GET** → `http://127.0.0.1:8000/api/tasks/`
Ответ: `200 OK`, пустой массив `[]`

### ✅ 2. Создать задачу

**POST** → `http://127.0.0.1:8000/api/tasks/`
**Headers:**

```
Content-Type: application/json
```

**Body (raw JSON):**

```json
{
  "title": "Купить продукты",
  "description": "Молоко, хлеб, яйца",
  "completed": false
}
```

### ✅ 3. Получить задачу по ID

**GET** → `http://127.0.0.1:8000/api/tasks/1/`

### ✅ 4. Обновить задачу

**PUT** → `http://127.0.0.1:8000/api/tasks/1/`
**Body:**

```json
{
  "title": "Купить продукты",
  "description": "Молоко, хлеб, яйца, сыр, масло",
  "completed": true
}
```

### ✅ 5. Удалить задачу

**DELETE** → `http://127.0.0.1:8000/api/tasks/1/`

---

## 🔍 Browsable API

Можно использовать встроенный интерфейс DRF:
Откройте в браузере → [http://127.0.0.1:8000/api/tasks/](http://127.0.0.1:8000/api/tasks/)
Можно добавлять, редактировать и удалять задачи прямо из браузера!

---

## ✅ Чек-лист

* [x] Python установлен
* [x] Виртуальное окружение создано
* [x] Django и DRF установлены
* [x] Проект и приложение созданы
* [x] Настройки внесены
* [x] Миграции применены
* [x] Сервер запущен
* [x] API протестировано в Postman

---

## 🐛 Возможные ошибки

| Проблема                           | Решение                                                                 |
| ---------------------------------- | ----------------------------------------------------------------------- |
| `No module named 'rest_framework'` | `pip install djangorestframework`                                       |
| `Table doesn't exist`              | `python manage.py makemigrations && python manage.py migrate`           |
| `404 Not Found`                    | Проверьте `urls.py` (должен быть `path('api/', include('tasks.urls'))`) |
| Порт 8000 занят                    | `python manage.py runserver 8080`                                       |

---

## 🎓 Дополнительные ресурсы

* [Django Docs](https://docs.djangoproject.com/)
* [DRF Docs](https://www.django-rest-framework.org/)
* [Postman Docs](https://learning.postman.com/)
---
