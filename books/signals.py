# books/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Book
from .utils import unique_slugify

@receiver(pre_save, sender=Book)
def book_pre_save_slug(sender, instance: Book, **kwargs):
    # якщо slug уже є – нічого не робимо
    if instance.slug:
        return
    instance.slug = unique_slugify(instance)
    # маячок для models.save(), щоб воно не робило те саме
    setattr(instance, "_slug_from_signal", True)
