from ..models import BillMaster


class BillSelector:

    @staticmethod
    def get_all():
        return BillMaster.objects.select_related(
            "property",
            "outlet",
            "bill_type",
            "source_module",
            "order",
            "guest",
            "room",
            "stay",
            "folio",
            "discount_type",
            "tax_type",
            "created_by",
        ).all()

    @staticmethod
    def get_by_id(pk):
        return BillSelector.get_all().get(pk=pk)
