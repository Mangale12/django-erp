from decimal import Decimal, InvalidOperation

from django.db import transaction

from hotel_app.restaurant_menu.forms.bill_master_form import BillMasterForm
from hotel_app.restaurant_menu.models import BillMaster


class BillService:
    @staticmethod
    def _to_decimal(value, fallback=Decimal("0.00")):
        try:
            if value in (None, ""):
                return fallback
            return Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            return fallback

    @staticmethod
    def generate_bill_number():
        base_prefix = "BILL-"
        latest = BillMaster.objects.order_by("-id").first()
        next_seq = (latest.id + 1) if latest else 1
        candidate = f"{base_prefix}{next_seq:06d}"

        while BillMaster.objects.filter(bill_no=candidate).exists():
            next_seq += 1
            candidate = f"{base_prefix}{next_seq:06d}"
        return candidate

    @classmethod
    def _compute_totals(cls, bill_master):
        sub_total = cls._to_decimal(bill_master.sub_total)
        discount_amount = cls._to_decimal(bill_master.discount_value)
        extra_charge = cls._to_decimal(bill_master.extra_charge_amount)
        service_charge = cls._to_decimal(bill_master.service_charge_amount)
        round_off = cls._to_decimal(bill_master.round_off)

        taxable_amount = sub_total - discount_amount + extra_charge + service_charge
        tax_rate = cls._to_decimal(getattr(bill_master.tax_type, "tax_rate", 0))
        tax_amount = (taxable_amount * tax_rate) / Decimal("100.00")

        bill_master.discount_amount = discount_amount
        bill_master.tax_amount = tax_amount
        bill_master.grand_total = taxable_amount + tax_amount + round_off
        return bill_master

    @classmethod
    def create(cls, post_data, user=None):
        with transaction.atomic():
            form = BillMasterForm(post_data)
            if not form.is_valid():
                return None, form

            bill_master = form.save(commit=False)
            if not bill_master.bill_no:
                bill_master.bill_no = cls.generate_bill_number()
            if user and user.is_authenticated:
                bill_master.created_by = user

            cls._compute_totals(bill_master)
            bill_master.save()
            return bill_master, form

    @classmethod
    def update(cls, bill_master, post_data):
        with transaction.atomic():
            form = BillMasterForm(post_data, instance=bill_master)
            if not form.is_valid():
                return None, form

            bill_master = form.save(commit=False)
            if not bill_master.bill_no:
                bill_master.bill_no = cls.generate_bill_number()

            cls._compute_totals(bill_master)
            bill_master.save()
            return bill_master, form
