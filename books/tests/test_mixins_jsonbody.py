from django.test import TestCase, RequestFactory
from books.mixins import JSONBodyMixin
from django.views import View

class _JsonView(JSONBodyMixin, View):
    pass

class JSONBodyMixinTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_parse_json_body(self):
        req = self.rf.post("/fake/", data='{"a": 1, "b": "x"}', content_type="application/json")
        v = _JsonView()
        v.setup(req)
        data = v.parse_json_body()
        assert data == {"a": 1, "b": "x"}
