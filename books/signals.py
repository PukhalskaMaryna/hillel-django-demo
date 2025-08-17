from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Book

@receiver(pre_save, sender=Book)
def set_book_slug(sender, instance, **kwargs):
    # якщо slug уже є — нічого не робимо
    if getattr(instance, "slug", None):
        return
    title = getattr(instance, "title", "")
    if not title:
        return
    base = slugify(title)
    slug = base or "book"
    i = 1
    while Book.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        i += 1
        slug = f"{base}-{i}"
    instance.slug = slug
