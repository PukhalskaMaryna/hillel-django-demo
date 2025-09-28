# dashboard/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages

from pathlib import Path
import os
import shutil
import json

from .custom_signals import file_uploaded, text_analyzed


def home(request):
    """
    Головна дашборда. Можеш створити шаблон:
    templates/dashboard/home.html
    (або лишити hello.html — тоді просто змінити ім'я тут)
    """
    # Якщо вже маєш hello.html — можеш повернути його:
    # return render(request, "dashboard/hello.html", {"title": "Dashboard"})
    return render(request, "dashboard/home.html", {"title": "Dashboard"})


def api_ping(request):
    """Простий healthcheck."""
    return JsonResponse({"status": "ok", "app": "dashboard"})


@require_POST
def api_echo(request):
    """
    Приймає JSON {"text": "..."} → повертає {"original": "...", "upper": "..."}.
    Додатково шле кастомний сигнал text_analyzed з метриками тексту.
    """
    try:
        data = json.loads((request.body or b"{}").decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid json"}, status=400)

    text = data.get("text", "")

    # Надсилаємо кастомний сигнал із метриками
    word_count = len(text.split())
    char_count = len(text)
    text_analyzed.send(
        sender=api_echo.__class__,
        request=request,
        words=word_count,
        chars=char_count,
        sample=text[:30],
    )

    return JsonResponse({"original": text, "upper": text.upper()})


def files_page(request):
    """
    Завантаження файлу в media/uploads та копія в media/backup.
    Після успіху: шлемо сигнал file_uploaded і показуємо Django messages.
    """
    uploads_dir = Path(settings.MEDIA_ROOT) / "uploads"
    backups_dir = Path(settings.MEDIA_ROOT) / "backup"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    backups_dir.mkdir(parents=True, exist_ok=True)

    if request.method == "POST":
        f = request.FILES.get("file")
        if not f:
            messages.error(request, "Файл не вибрано 🙈")
            return redirect("dashboard:files")

        try:
            # зберегти оригінал
            dest = uploads_dir / f.name
            with dest.open("wb+") as out:
                for chunk in f.chunks():
                    out.write(chunk)

            # створити копію в backup/
            shutil.copy2(dest, backups_dir / f.name)

            # кастомний сигнал (можна ловити у receivers.py)
            file_uploaded.send(
                sender=files_page.__class__,
                request=request,
                filename=f.name,
                size=dest.stat().st_size,
            )

            messages.success(request, f"«{f.name}» завантажено ✅ Копію створено у backup/")
        except Exception as e:
            messages.error(request, f"Не вдалося завантажити файл: {e}")

        # PRG: після POST — редирект, щоб не дублювати завантаження при refresh
        return redirect("dashboard:files")

    # GET: показуємо списки файлів
    def list_dir(path: Path):
        items = []
        if path.exists():
            for name in os.listdir(path):
                p = path / name
                if p.is_file():
                    rel = p.relative_to(settings.MEDIA_ROOT).as_posix()
                    items.append(
                        {
                            "name": name,
                            "size": p.stat().st_size,
                            "url": settings.MEDIA_URL + rel,
                        }
                    )
        return items

    context = {
        "uploads": list_dir(uploads_dir),
        "backups": list_dir(backups_dir),
    }
    return render(request, "dashboard/files.html", context)
