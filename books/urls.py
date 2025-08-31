# books/urls.py
from django.urls import path
from .views import bookstore_home, book_detail, BookListView  # без catalog

app_name = "books"

urlpatterns = [
    path("", bookstore_home, name="bookstore_home"),
    path("catalog/", BookListView.as_view(), name="book_catalog"),
    path("catalog/<slug:slug>/", book_detail, name="book_detail"),
]
