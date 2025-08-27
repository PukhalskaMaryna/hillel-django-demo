# books/mixins.py
from django.db.models import Q

class SearchQueryMixin:
    """Додає простий пошук за ?q=... до ListView."""
    query_param = "q"
    search_fields = ("title__icontains",)  # перелік полів для пошуку

    def get_query(self):
        return (self.request.GET.get(self.query_param) or "").strip()

    def filter_queryset(self, qs):
        q = self.get_query()
        if not q:
            return qs
        cond = Q()
        for f in self.search_fields:
            cond |= Q(**{f: q})
        return qs.filter(cond)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.get_query()
        # total через paginator (якщо є paginate_by)
        paginator = ctx.get("paginator")
        if paginator:
            ctx["total"] = paginator.count
        else:
            ctx["total"] = self.get_queryset().count()
        return ctx
