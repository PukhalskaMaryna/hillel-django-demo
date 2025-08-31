# books/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Book

class BookListView(ListView):
    model = Book
    template_name = "books/catalog.html"
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self):
        qs = Book.objects.all().order_by("-created_at")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(title__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = self.request.GET.get("q", "")
        ctx["q"] = q
        ctx["total"] = self.get_queryset().count()
        return ctx

def bookstore_home(request):
    return render(request, "books/home.html")

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, "books/detail.html", {"book": book})

# ===== DRF API =====
from rest_framework import viewsets, permissions, filters
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # для демо
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'slug']
    ordering_fields = ['created_at', 'price', 'title']
