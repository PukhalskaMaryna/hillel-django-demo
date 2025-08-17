# books/migrations/0002_book_slug.py
from django.db import migrations, models
from django.utils.text import slugify

def populate_slugs(apps, schema_editor):
    Book = apps.get_model('books', 'Book')
    for b in Book.objects.all().order_by('id'):
        base = slugify(b.title) or "book"
        slug = base
        i = 1
        # гарантуємо унікальність серед існуючих записів
        while Book.objects.filter(slug=slug).exclude(pk=b.pk).exists():
            i += 1
            slug = f"{base}-{i}"
        b.slug = slug
        b.save(update_fields=['slug'])

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(max_length=220, blank=True, null=True),  # без unique!
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
    ]
