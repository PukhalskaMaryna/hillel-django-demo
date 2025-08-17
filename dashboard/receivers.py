# dashboard/receivers.py
from django.dispatch import receiver
from django.contrib import messages
from .custom_signals import file_uploaded

@receiver(file_uploaded)
def on_file_uploaded(sender, request, filename, size, **kwargs):
    # мінімальна демонстрація: покажемо повідомлення користувачу
    if request:
        messages.info(request, f"Сигнал спрацював 📡: «{filename}» ({size} байт)")
