from django.db import models
from django.utils.text import slugify

class Author(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name="books")  # ⬅ NEW

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "book"
            slug = base
            i = 1
            while Book.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)
