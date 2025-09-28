from django.test import TestCase, RequestFactory
from books.models import Book
from books.mixins import PageSizeFromQueryMixin
from django.core.paginator import Paginator
from django.views.generic import ListView

class _PageSizeView(PageSizeFromQueryMixin, ListView):
    model = Book
    paginate_by = 10  # базове значення

class PageSizeMixinTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        for i in range(5):
            Book.objects.create(title=f"B{i}")

    def test_page_size_from_query(self):
        req = self.rf.get("/fake/?page_size=2")
        v = _PageSizeView()
        v.setup(req)
        qs = v.get_queryset().order_by('id')
        # емулюємо пагінацію так само, як у ListView
        paginator = Paginator(qs, v.get_paginate_by(qs))
        page = paginator.page(1)
        assert page.paginator.per_page == 2
        assert len(page.object_list) == 2
