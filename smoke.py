import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","myproject.settings")
import django
django.setup()
from django.test import Client
from books.models import Book
from django.db.models import Min
# гарантуємо хоч одну книгу
if not Book.objects.exists():
    from datetime import date
    Book.objects.create(title="Demo Book", author="System", published_date=date.today())
c = Client()
def ok(u):
    r = c.get(u)
    print(f"[{r.status_code}] {u}")
    assert r.status_code == 200, (u, r.status_code)
ok("/")
ok("/api/books/")
bid = Book.objects.aggregate(Min("id"))["id__min"] or 1
ok(f"/books/{bid}/")
print("✅ smoke OK (python file)")
