from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    fields = (
        ('status', 'id'),
        ('first_name', 'last_name'),
        ('email', 'address'),
        'basket_history',
        ('created', 'initiator')
    )
    readonly_fields = ('id', 'created', 'initiator')
