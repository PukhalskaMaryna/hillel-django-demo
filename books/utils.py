# books/utils.py
from django.utils.text import slugify

def unique_slugify(instance, source_field='title', slug_field='slug', fallback='book'):
    Model = instance.__class__
    base = slugify(getattr(instance, source_field) or '') or fallback
    slug = base
    i = 1
    # уникаємо зіткнень (крім свого pk)
    while Model.objects.filter(**{slug_field: slug}).exclude(pk=instance.pk).exists():
        i += 1
        slug = f"{base}-{i}"
    return slug