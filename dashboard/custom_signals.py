# dashboard/custom_signals.py
from django.dispatch import Signal

# наш простий сигнал про завантаження файлу
file_uploaded = Signal()
