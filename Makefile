PY=python
MANAGE=$(PY) manage.py

export DJANGO_SECRET_KEY?=$(shell grep -E '^DJANGO_SECRET_KEY=' .env | cut -d= -f2-)
export DEBUG?=$(shell grep -E '^DEBUG=' .env | cut -d= -f2-)

.PHONY: run migrate makemigrations superuser smoke shell collect

run:
	$(MANAGE) runserver 127.0.0.1:8000

makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(PY) - <<'PY'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","myproject.settings")
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
u, created = User.objects.get_or_create(username="admin", defaults={"is_staff":True,"is_superuser":True})
if created:
    u.set_password("admin12345")
    u.email = "admin@example.com"
    u.save()
    print("✅ admin / admin12345 створено")
else:
    print("ℹ️ admin вже існує")
PY

smoke:
	$(PY) - <<'PY'
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
    assert r.status_code==200, (u, r.status_code, r.content[:200])

ok("/")
ok("/api/books/")
bid = Book.objects.aggregate(Min("id"))["id__min"] or 1
ok(f"/books/{bid}/")
print("✅ smoke OK")
PY

shell:
	$(MANAGE) shell

collect:
	$(MANAGE) collectstatic --noinput
