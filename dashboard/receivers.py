# dashboard/receivers.py
from django.dispatch import receiver
from django.contrib import messages
from .custom_signals import file_uploaded, text_analyzed

@receiver(file_uploaded)
def on_file_uploaded(sender, request, filename, size, **kwargs):
    print(f"[signal] file_uploaded: {filename} ({size} bytes)")
    messages.info(request, f"Сигнал спрацював 📡: «{filename}» ({size} байт)")

@receiver(text_analyzed)
def on_text_analyzed(sender, request, words, chars, sample, **kwargs):
    print(f"[signal] text_analyzed: words={words}, chars={chars}, sample={sample!r}")
    # Для AJAX-поста повідомлення побачиш після наступного переходу на сторінку
    try:
        messages.info(request, f"Аналіз тексту: {words} слів, {chars} символів")
    except Exception:
        pass
