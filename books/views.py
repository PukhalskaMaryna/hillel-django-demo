from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Book
from django.views.generic import ListView
from .mixins import SearchQueryMixin
from .models import Book

def bookstore_home(request):
    return render(request, "books/home.html", {})


class BookListView(SearchQueryMixin, ListView):
    model = Book
    template_name = "books/catalog.html"
    context_object_name = "books"
    paginate_by = 10
    def get_queryset(self):
        return self.filter_queryset(super().get_queryset())
    
    
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



class BookListView(SearchQueryMixin, ListView):
    model = Book
    template_name = "books/catalog.html"
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().order_by("-created_at")
        return self.filter_queryset(qs)