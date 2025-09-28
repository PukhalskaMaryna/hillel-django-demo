from django.test import TestCase, RequestFactory
from books.models import Book
from books.mixins import CSVExportMixin
from django.views.generic import ListView

class _CsvView(CSVExportMixin, ListView):
    model = Book
    list_display = ["id", "title"]  # колонки у CSV

class CSVExportMixinTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        Book.objects.create(title="Alpha")
        Book.objects.create(title="Beta")

    def test_csv_export(self):
        req = self.rf.get("/fake/?format=csv")
        v = _CsvView()
        v.setup(req)
        resp = v.get(req)
        assert resp.status_code == 200
        assert resp["Content-Type"].startswith("text/csv")
        body = resp.content.decode("utf-8")
        assert "title" in body and "Alpha" in body
