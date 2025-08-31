# books/urls.py
from django.urls import path
from .views import (
    bookstore_home,
    BookListView, BookDetailView, BookCreateView,
    BookApiCreateView, BooksReportView
)

app_name = "books"

urlpatterns = [
    path("", bookstore_home, name="bookstore_home"),
    path("catalog/", BookListView.as_view(), name="book_catalog"),
    path("catalog/add/", BookCreateView.as_view(), name="book_add"),
    path("catalog/<slug:slug>/", BookDetailView.as_view(), name="book_detail"),

    # API/Staff демо
    path("api/create/", BookApiCreateView.as_view(), name="api_book_create"),
    path("reports/", BooksReportView.as_view(), name="reports"),
]
