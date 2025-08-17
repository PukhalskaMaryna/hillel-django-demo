# dashboard/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST   # ← ДОДАНО
import json 
from django.conf import settings
from pathlib import Path
import os
import shutil
from django.contrib import messages
from .custom_signals import file_uploaded




def hello(request):
    return render(request, "dashboard/hello.html", {"title": "Dashboard Hello"})

def api_ping(request):
    return JsonResponse({"status": "ok", "app": "dashboard"})

@require_POST
def api_echo(request):
    try:
        data = json.loads((request.body or b"{}").decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid json"}, status=400)
    text = data.get("text", "")
    return JsonResponse({"original": text, "upper": text.upper()})

def files_page(request):
    uploads_dir = Path(settings.MEDIA_ROOT) / 'uploads'
    backups_dir = Path(settings.MEDIA_ROOT) / 'backup'
    uploads_dir.mkdir(parents=True, exist_ok=True)
    backups_dir.mkdir(parents=True, exist_ok=True)

    if request.method == 'POST':
        f = request.FILES.get('file')
        if not f:
            messages.error(request, "Файл не вибрано 🙈")
            return redirect('dashboard:files')

        try:
            dest = uploads_dir / f.name
            with dest.open('wb+') as out:
                for chunk in f.chunks():
                    out.write(chunk)

            shutil.copy2(dest, backups_dir / f.name)
            # після успішного копіювання
            file_uploaded.send(
                sender=files_page.__class__,
                request=request,
                filename=f.name,
                size=dest.stat().st_size
            )

            messages.success(request, f"«{f.name}» завантажено ✅ Копію створено у backup/")
        except Exception as e:
            messages.error(request, f"Не вдалося завантажити файл: {e}")
        return redirect('dashboard:files')  # Post/Redirect/Get

    # список файлів (GET)
    def list_dir(path: Path):
        items = []
        if path.exists():
            for name in os.listdir(path):
                p = path / name
                if p.is_file():
                    rel = p.relative_to(settings.MEDIA_ROOT).as_posix()
                    items.append({"name": name, "size": p.stat().st_size, "url": settings.MEDIA_URL + rel})
        return items

    context = {"uploads": list_dir(uploads_dir), "backups": list_dir(backups_dir)}
    return render(request, "dashboard/files.html", context)

