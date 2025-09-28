# dashboard/urls.py
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # Головна сторінка (іменований маршрут 'home' для base.html)
    path("", views.home, name="home"),

    # Сумісність зі старою адресою /hello (необов'язково, можна прибрати)
    path("hello/", views.home, name="hello"),

    # API-сервіси
    path("api/ping/", views.api_ping, name="ping"),
    path("api/echo/", views.api_echo, name="echo"),

    # Завантаження і перегляд файлів
    path("files/", views.files_page, name="files"),
]
