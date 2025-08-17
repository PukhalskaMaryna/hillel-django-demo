# books/migrations/0003_alter_book_slug.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.SlugField(max_length=220, unique=True),  # без null=True і blank=True
        ),
    ]
