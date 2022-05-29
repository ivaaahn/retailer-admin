from django import forms
from django.contrib import admin

from shops.models import ShopModel


def shop_address(obj):
    return obj.address


shop_address.short_description = "Адрес магазина"
shop_address.admin_order_field = "address__city"


class StaffInlineAdmin(admin.TabularInline):
    model = ShopModel.staff.through
    verbose_name = "Сотрудник магазина"
    verbose_name_plural = "Сотрудники магазина"


@admin.register(ShopModel)
class ShopAdmin(admin.ModelAdmin):
    list_display = (shop_address, "id")
    sortable_by = ("id", shop_address)
    inlines = (StaffInlineAdmin,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(pk__in=request.user.shop_set.all())
        return qs
