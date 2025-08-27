# books/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
import json

from .models import Book
from .mixins import SearchQueryMixin


def bookstore_home(request):
    return render(request, "books/home.html")


class BookListView(SearchQueryMixin, ListView):
    model = Book
    template_name = "books/catalog.html"
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().order_by("-created_at")
        return self.filter_queryset(qs)


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, "books/detail.html", {"book": book})


@require_POST
def api_book_create(request):
    """
    Приймає JSON {"title": "...", "price": "..."} → створює Book і повертає дані.
    """
    try:
        data = json.loads((request.body or b"{}").decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid_json"}, status=400)

    title = (data.get("title") or "").strip()
    price_raw = (str(data.get("price") or "")).strip()

    if not title:
        return JsonResponse({"error": "title_required"}, status=400)

    try:
        price = Decimal(price_raw)
    except InvalidOperation:
        return JsonResponse({"error": "bad_price"}, status=400)

    if price < 0:
        return JsonResponse({"error": "price_negative"}, status=400)

    book = Book.objects.create(title=title, price=price)  # slug згенерується в save/signals

    return JsonResponse(
        {"ok": True, "slug": book.slug, "title": book.title, "price": str(book.price)}
    )
