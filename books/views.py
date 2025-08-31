# books/views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from .models import Book
from .mixins import (
    SearchQueryMixin, PageSizeFromQueryMixin, OrderingMixin,
    CSVExportMixin, SelectPrefetchMixin, BreadcrumbsMixin,
    SuccessMessageMixinLite, JSONBodyMixin, StaffRequiredMixin, CacheControlMixin
)

# Головна книгарні (твій існуючий FBV можна лишити як є)
def bookstore_home(request):
    return render(request, "books/home.html")

class BookListView(PageSizeFromQueryMixin,
                   OrderingMixin,
                   SearchQueryMixin,
                   CSVExportMixin,
                   SelectPrefetchMixin,
                   CacheControlMixin,      # bonus: no-store для динаміки
                   ListView):
    model = Book
    template_name = "books/catalog.html"
    context_object_name = "books"

    # Ordering
    default_ordering = "-created_at"
    allowed_order_fields = ("created_at", "title", "price")

    # Pagination
    default_page_size = 10
    max_page_size = 50
    paginate_by = 10

    # CSV
    csv_filename = "books.csv"
    csv_fields = ("title", "price", "created_at", "slug")

    # Search
    search_fields = ("title__icontains", "slug__icontains")

    # Cache
    cache_control = "no-store"

    def get_queryset(self):
        qs = super().get_queryset().order_by(self.get_ordering() or "-created_at")
        return self.filter_queryset(qs)


class BookDetailView(BreadcrumbsMixin, DetailView):
    model = Book
    template_name = "books/detail.html"
    context_object_name = "book"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_breadcrumbs(self):
        obj = self.get_object()
        return [
            ("Книги", "/books/"),
            ("Каталог", "/books/catalog/"),
            (obj.title, ""),
        ]


class BookCreateView(SuccessMessageMixinLite, CreateView):
    model = Book
    fields = ("title", "price")  # slug заповниться автоматично
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:book_catalog")
    success_message = "Книгу «{object}» створено!"

# API-приклад на CBV з JSONBodyMixin (для AJAX/інтеграцій)
class BookApiCreateView(JSONBodyMixin, View):
    def post(self, request, *args, **kwargs):
        data = self.parse_json_body()
        title = (data.get("title") or "").strip()
        price = data.get("price")
        if not title or price is None:
            return JsonResponse({"error": "title та price обов'язкові"}, status=400)
        try:
            obj = Book.objects.create(title=title, price=price)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"id": obj.id, "slug": obj.slug, "title": obj.title, "price": str(obj.price)}, status=201)

# Staff-only сторінка (демо StaffRequiredMixin)
class BooksReportView(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # мінімальний демо-контент
        total = Book.objects.count()
        return JsonResponse({"report": "ok", "total_books": total})
