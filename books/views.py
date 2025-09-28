from django.shortcuts import render, get_object_or_404
from .models import Book

def book_list(request):
    books = Book.objects.order_by("-id")
    return render(request, "books/list.html", {"books": books})

def book_detail(request, pk: int):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "books/detail.html", {"book": book})

from django.conf import settings
import os

def files_list(request):
    root = settings.MEDIA_ROOT
    tree = []
    if os.path.isdir(root):
        for dirpath, dirnames, filenames in os.walk(root):
            rel = os.path.relpath(dirpath, root)
            rel = "" if rel == "." else (rel.replace("\\","/") + "/")
            tree.append((rel, sorted(filenames)))
    return render(request, "files/list.html", {"MEDIA_URL": settings.MEDIA_URL, "MEDIA_ROOT": str(root), "tree": tree})
