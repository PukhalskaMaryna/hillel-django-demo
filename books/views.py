from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Book  # якщо ще нема моделі — тимчасово прибери

def bookstore_home(request):
    return render(request, "books/home.html", {})


def catalog(request):
    q = (request.GET.get("q") or "").strip()
    qs = Book.objects.all().order_by("title")
    if q:
        qs = qs.filter(title__icontains=q)

    paginator = Paginator(qs, 10)              # 10 книг на сторінку
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # щоб не ламати шаблон: 'books' = page_obj (ітерабельний)
    return render(request, "books/catalog.html", {
        "books": page_obj,
        "page_obj": page_obj,
        "q": q,
        "total": paginator.count,
    })

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, "books/detail.html", {"book": book})
