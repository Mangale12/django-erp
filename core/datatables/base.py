from django.views import View
from django.http import JsonResponse
from django.db.models import Q

class BaseDataTable(View):
    model = None            # Child table must define
    columns = []            # List of columns to show
    search_fields = []      # List of fields for search
    actions = None          # ActionGroup instance (optional)

    def get_queryset(self):
        """
        Child table can override this to return a custom queryset
        (joins, annotations, filters)
        """
        return self.model.objects.all()

    def filter_queryset(self, qs, search):
        """Generic search filter"""
        if not search:
            return qs

        query = Q()
        for field in self.search_fields:
            query |= Q(**{f"{field}__icontains": search})
        return qs.filter(query)

    def get_field_value(self, obj, field_name):
        """
        Generic field resolver:
        - ForeignKeys → __str__ automatically
        - Boolean → yes/no
        - Date → formatted string
        """
        val = getattr(obj, field_name, "")

        # Boolean fields
        if isinstance(val, bool):
            return "Yes" if val else "No"

        # Date fields
        if hasattr(val, "strftime"):
            return val.strftime("%Y-%m-%d")

        # ForeignKey or any object with __str__
        if hasattr(val, "__class__") and hasattr(val, "__str__"):
            return str(val)

        return val

    def get_row_data(self, obj):
        """
        Default row builder
        Child table can override this for custom logic
        """
        row = {col: self.get_field_value(obj, col) for col in self.columns}

        if self.actions:
            row["actions"] = self.actions.render(obj)

        return row

    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search = request.GET.get("search[value]", "")

        qs = self.get_queryset()
        records_total = qs.count()

        qs = self.filter_queryset(qs, search)
        records_filtered = qs.count()

        qs = qs[start:start + length]

        data = [self.get_row_data(obj) for obj in qs]

        return JsonResponse({
            "draw": draw,
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered,
            "data": data,
        })
