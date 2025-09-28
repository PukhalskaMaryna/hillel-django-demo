from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120, blank=True, default="")
    published_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.title
