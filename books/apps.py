# books/apps.py
from __future__ import annotations

from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "books"
    verbose_name = "Books"

    # Якщо захочеш реєструвати сигнали тут — розкоментуй ready()
    # і прибери імпорт сигналів із models.py, щоб не було дублю.
    #
    # def ready(self) -> None:
    #     from . import signals  # noqa: F401
    #     return super().ready()
