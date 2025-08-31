# books/mixins.py
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q
import csv, json

class SearchQueryMixin:
    """Фільтрує queryset за ?q=... (по вказаних полях)."""
    search_param = "q"
    search_fields = ("title__icontains",)

    def filter_queryset(self, qs):
        q = (self.request.GET.get(self.search_param) or "").strip()
        self._q_value = q
        if not q:
            return qs
        cond = Q()
        for f in self.search_fields:
            cond |= Q(**{f: q})
        return qs.filter(cond)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = getattr(self, "_q_value", "")
        total = getattr(ctx.get("page_obj"), "paginator", None)
        ctx["total"] = getattr(total, "count", None)
        return ctx


class PageSizeFromQueryMixin:
    """Задає paginate_by із ?page_size=... (зі стелею)."""
    page_size_param = "page_size"
    default_page_size = 10
    max_page_size = 100

    def get_paginate_by(self, queryset):
        raw = self.request.GET.get(self.page_size_param)
        if not raw:
            return getattr(self, "paginate_by", self.default_page_size)
        try:
            n = max(1, min(int(raw), self.max_page_size))
        except ValueError:
            n = self.default_page_size
        self.paginate_by = n
        return n


class OrderingMixin:
    """Сортування за ?order=field або -field (білий список)."""
    order_param = "order"
    default_ordering = None
    allowed_order_fields = ()

    def get_ordering(self):
        order = self.request.GET.get(self.order_param)
        allowed = set(self.allowed_order_fields) | {f"-{f}" for f in self.allowed_order_fields}
        if order and (not allowed or order in allowed):
            return order
        return self.default_ordering


class CSVExportMixin:
    """Якщо ?format=csv — повертає CSV замість HTML."""
    csv_param = "format"
    csv_value = "csv"
    csv_filename = "export.csv"
    csv_fields = ()  # якщо пусто — всі поля моделі

    def render_to_csv(self, qs):
        model = qs.model
        fields = self.csv_fields or [f.name for f in model._meta.fields]
        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = f'attachment; filename="{self.csv_filename}"'
        w = csv.writer(resp)
        w.writerow(fields)
        for obj in qs:
            w.writerow([getattr(obj, f) for f in fields])
        return resp

    def get(self, request, *args, **kwargs):
        if request.GET.get(self.csv_param) == self.csv_value:
            self.object_list = self.get_queryset()
            return self.render_to_csv(self.object_list)
        return super().get(request, *args, **kwargs)


class StaffRequiredMixin(AccessMixin):
    """Доступ лише для staff."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class JSONBodyMixin:
    """Акуратний парсер JSON-тіла в self.json_data."""
    json_data = None
    def parse_json_body(self):
        if self.json_data is not None:
            return self.json_data
        try:
            body = (self.request.body or b"").decode("utf-8")
            self.json_data = json.loads(body) if body else {}
        except Exception:
            self.json_data = {}
        return self.json_data


class SuccessMessageMixinLite:
    """messages.success() після form_valid()."""
    success_message = ""
    def form_valid(self, form):
        resp = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message.format(object=self.object))
        return resp


class SelectPrefetchMixin:
    """Оптимізація запитів через select_related/prefetch_related."""
    select_related = ()
    prefetch_related = ()
    def get_queryset(self):
        qs = super().get_queryset()
        if self.select_related:
            qs = qs.select_related(*self.select_related)
        if self.prefetch_related:
            qs = qs.prefetch_related(*self.prefetch_related)
        return qs


class CacheControlMixin:
    """Додає заголовок Cache-Control (напр., 'no-store')."""
    cache_control = "no-store"
    def dispatch(self, request, *args, **kwargs):
        resp = super().dispatch(request, *args, **kwargs)
        try:
            resp["Cache-Control"] = self.cache_control
        except Exception:
            pass
        return resp


class BreadcrumbsMixin:
    """Прокидає breadcrumbs у контекст."""
    breadcrumbs = []  # список кортежів (label, url)
    def get_breadcrumbs(self):
        return self.breadcrumbs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["breadcrumbs"] = self.get_breadcrumbs()
        return ctx
