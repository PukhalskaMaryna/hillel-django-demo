# books/utils.py
from django.utils.text import slugify

def unique_slugify(instance, value, slug_field_name: str = "slug", slug_separator: str = "-") -> str:
    """
    Згенерувати унікальний slug для instance на базі value.
    Якщо slug уже зайнятий, додає -1, -2, ... доки не стане унікальним.
    Повертає встановлений slug і також прописує його в instance.<slug_field_name>.
    """
    base = slugify(value) or "item"
    slug = base
    ModelClass = instance.__class__
    i = 1
    # Уникаємо конфлікту із самим собою (exclude pk)
    qs = ModelClass._default_manager.all()
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)

    while qs.filter(**{slug_field_name: slug}).exists():
        slug = f"{base}{slug_separator}{i}"
        i += 1

    setattr(instance, slug_field_name, slug)
    return slug
