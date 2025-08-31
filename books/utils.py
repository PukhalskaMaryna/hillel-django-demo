# books/utils.py
from django.utils.text import slugify

def unique_slugify(instance, value, slug_field_name='slug', queryset=None):
    base = slugify(value) or "book"
    slug = base
    Model = instance.__class__
    if queryset is None:
        queryset = Model.objects.all()

    i = 1
    # шукаємо в базі, щоб уникнути колізій
    while queryset.filter(**{slug_field_name: slug}).exclude(pk=instance.pk).exists():
        i += 1
        slug = f"{base}-{i}"
    return slug
