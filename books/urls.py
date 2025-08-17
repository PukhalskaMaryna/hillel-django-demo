# books/urls.py
from django.urls import path
from .views import bookstore_home, catalog, book_detail  # ⬅ додай book_detail

urlpatterns = [
    path("", bookstore_home, name="bookstore_home"),
    path("catalog/", catalog, name="book_catalog"),
    path("catalog/<slug:slug>/", book_detail, name="book_detail"),
]
