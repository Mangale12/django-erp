from django.db import models
from django.utils.timezone import now
from django.conf import settings
from hotel_app.rooms.models import Room


class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('open', 'Open'),
        ('kot-sent', 'KOT Sent'),
        ('partial-served', 'Partial Served'),
        ('billed', 'Billed'),
        ('closed', 'Closed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    table = models.ForeignKey(
        'restaurant_menu.TableSetup',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='orders'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='orders'
    )

    order_number = models.CharField(max_length=100, unique=True)
    guest_count = models.IntegerField(default=1)

    room = models.ForeignKey(
        Room,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='orders'
    )

    guest_name = models.CharField(max_length=100)
    order_start_time = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user_display = self.user.get_username() if self.user else "Guest"
        return f"Order {self.id} - {user_display}"


class OrderItem(models.Model):
    ORDER_ITEM_STATUS = (
        ('ordered', 'Ordered'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled'),
    )

    order = models.ForeignKey(
        'restaurant_menu.Order',
        on_delete=models.CASCADE,
        related_name='order_items'
    )

    menu_item = models.ForeignKey(
        'restaurant_menu.MenuItem',
        on_delete=models.CASCADE,
        related_name='order_items'
    )

    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    modifiers = models.ManyToManyField(
        'restaurant_menu.Modifier',
        through='restaurant_menu.OrderItemModifier',
        related_name='order_items'
    )

    order_item_status = models.CharField(max_length=20, choices=ORDER_ITEM_STATUS, default='ordered')
    cancel_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItemModifier(models.Model):
    order_item = models.ForeignKey(
        'restaurant_menu.OrderItem',
        on_delete=models.CASCADE,
        related_name='order_item_modifiers'
    )

    modifier = models.ForeignKey(
        'restaurant_menu.Modifier',
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('order_item', 'modifier')
