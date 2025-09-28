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


# === Token page (отримання токена за логін/пароль) ===
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.authtoken.models import Token

def token_page(request):
    token_value = None
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            token_value = token.key
        else:
            error = "Невірний логін або пароль"
    return render(request, "token_page.html", {"token": token_value, "error": error})

# === Token page (отримання DRF-токена за логін/пароль) ===
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.authtoken.models import Token

def token_page(request):
    token_value = None
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            token_value = token.key
        else:
            error = "Невірний логін або пароль"
    return render(request, "token_page.html", {"token": token_value, "error": error})
