from django.test import TestCase, RequestFactory
from books.models import Book
from books.mixins import SearchQueryMixin
from django.views.generic import ListView

class _TestListView(SearchQueryMixin, ListView):
    model = Book
    search_fields = ["title__icontains"]

class SearchQueryMixinTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        Book.objects.create(title="Python 101")
        Book.objects.create(title="Django Deep Dive")
        Book.objects.create(title="History of Art")

    def test_filters_by_q_param(self):
        req = self.rf.get("/fake/?q=Python")
        view = _TestListView()
        view.setup(req)
        base_qs = view.get_queryset()
        qs = view.filter_queryset(base_qs)  # ключова зміна
        titles = {b.title for b in qs}
        assert "Python 101" in titles
        assert "Django Deep Dive" not in titles
