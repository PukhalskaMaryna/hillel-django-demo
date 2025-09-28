from typing import Any, Optional

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Кастомні сигнали цього застосунку
from .custom_signals import file_uploaded, text_analyzed


# ---------- Кастомні сигнали dashboard ----------

@receiver(file_uploaded)
def on_file_uploaded(sender: Any, request: Optional[Any] = None, filename: str = "", size: int = 0, **kwargs):
    """
    Реакція на завантаження файлу: лог + флеш-повідомлення, якщо є request.
    """
    print(f"[signal] file_uploaded: {filename} ({size} bytes)")
    try:
        if request is not None:
            messages.info(request, f"Сигнал спрацював 📡: «{filename}» ({size} байт)")
    except Exception:
        # messages можуть не працювати в нетипових контекстах (тести/CLI)
        pass


@receiver(text_analyzed)
def on_text_analyzed(
    sender: Any,
    request: Optional[Any] = None,
    words: int = 0,
    chars: int = 0,
    sample: str = "",
    **kwargs,
):
    """
    Реакція на аналіз тексту: лог + флеш-повідомлення (буде видно після наступного HTTP-запиту).
    """
    print(f"[signal] text_analyzed: words={words}, chars={chars}, sample={sample!r}")
    try:
        if request is not None:
            messages.info(request, f"Аналіз тексту: {words} слів, {chars} символів")
    except Exception:
        pass


# ---------- Авто-створення DRF токена для нових користувачів ----------

try:
    # Імпортуємо тут, щоб файл залишався працездатним навіть без rest_framework.authtoken у INSTALLED_APPS
    from rest_framework.authtoken.models import Token  # type: ignore
except Exception:
    Token = None  # type: ignore[misc]


@receiver(post_save, sender=get_user_model())
def create_auth_token_for_new_user(sender, instance, created: bool, **kwargs):
    """
    При створенні нового користувача — видати/знайти DRF Token.
    Працює, якщо 'rest_framework.authtoken' є в INSTALLED_APPS (у нас є).
    """
    if not created or Token is None:
        return
    # get_or_create на випадок одночасних сигналів/міграцій
    Token.objects.get_or_create(user=instance)
