# books/signals.py
from __future__ import annotations

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Book


def _unique_slugify(
    instance: Book,
    value: str,
    slug_field_name: str = "slug",
    max_length: int = 220,
) -> str:
    """
    Будує унікальний slug на основі value:
    - slugify(value) з обрізанням до max_length
    - перевірка колізій з урахуванням instance.pk
    - додає -2, -3, ... поки не стане унікальним
    """
    base = slugify(value).strip("-") or "book"
    base = base[:max_length]
    slug = base

    Model = instance.__class__
    i = 2
    while (
        Model.objects.filter(**{slug_field_name: slug})
        .exclude(pk=instance.pk)
        .exists()
    ):
        suffix = f"-{i}"
        slug = f"{base[: max_length - len(suffix)]}{suffix}"
        i += 1
    return slug


@receiver(pre_save, sender=Book)
def book_pre_save_set_slug(sender, instance: Book, **kwargs) -> None:
    """
    Встановлюємо slug лише коли він порожній (не перезаписуємо при оновленні).
    """
    if not instance.slug:
        title = instance.title or (str(instance.pk) if instance.pk else "book")
        instance.slug = _unique_slugify(instance, title)
