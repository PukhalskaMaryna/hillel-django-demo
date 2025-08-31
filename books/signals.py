# books/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Book
from .utils import unique_slugify

@receiver(pre_save, sender=Book)
def book_pre_save_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slugify(instance, instance.title)
