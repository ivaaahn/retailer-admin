from django.contrib import admin

from order.models import OrderModel
from products.models import ProductModel


class OrderProductInlineAdmin(admin.StackedInline):
    model = OrderModel.products.through
    verbose_name = "Продукт данной категории"
    verbose_name_plural = "Продукты данной категории"
    can_delete = False
    extra = 0
    readonly_fields = (
        "product",
        "price",
        "qty",
    )

    def photo_preview(self, obj):
        return obj.photo_preview

    photo_preview.short_description = "Фото продукта"
    photo_preview.allow_tags = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = ProductModel.objects.select_related("category").all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "shop",
        "total_price",
        "receive_kind",
        "status",
        "created_at",
        "id",
    )
    inlines = (OrderProductInlineAdmin,)
    readonly_fields = ("user", "shop", "address")

    def get_queryset(self, request):
        qs = (
            super()
            .get_queryset(request)
            .prefetch_related("products")
            .select_related("user", "shop", "address", "shop__address")
        )
        if not request.user.is_superuser:
            qs = qs.filter(shop__in=request.user.shop_set.all())

        return qs
