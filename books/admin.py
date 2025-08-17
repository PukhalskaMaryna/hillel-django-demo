from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "created_at")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}  # можна руками правити перед збереженням
