import redis
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from products.models import ProductModel
from shop_products.models import ShopProductModel
from shops.models import ShopModel

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


class ShopProductsFilter(SimpleListFilter):
    title = "моим магазинам"  # a label for our filter
    parameter_name = "pages"  # you can put anything here

    def lookups(self, request, model_admin):
        res = []

        for shop in ShopModel.objects.filter(pk__in=request.user.shop_set.all()):
            res.append(
                (
                    shop.id,
                    str(shop),
                )
            )

        return res

    def queryset(self, request, queryset):
        if self.value():
            return queryset.distinct().filter(shop=self.value())

        return queryset.distinct().filter(shop__in=request.user.shop_set.all())


def product_name(obj):
    return obj.product.name


def product_category(obj):
    return obj.product.category


def shop(obj):
    return str(obj.shop)


product_name.short_description = "Наименование"
product_name.admin_order_field = "product__name"
product_category.short_description = "Категория"
product_category.admin_order_field = "product__category__name"
shop.short_description = "Магазин"
shop.admin_order_field = "shop__pk"


@admin.register(ShopProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        product_name,
        shop,
        product_category,
        "price",
        "qty",
    )

    list_filter = (
        "product__category",
        ShopProductsFilter,
    )

    def get_queryset(self, request):
        qs = (
            super()
            .get_queryset(request)
            .select_related("shop", "product", "shop__address", "product__category")
        )
        if not request.user.is_superuser:
            qs = qs.filter(shop__in=request.user.shop_set.all())
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shop":
            qs = ShopModel.objects.select_related("address").all()

            if not request.user.is_superuser:
                qs.filter(pk__in=request.user.shop_set.all())

            kwargs["queryset"] = qs

        if db_field.name == "product":
            kwargs["queryset"] = ProductModel.objects.select_related("category").all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @staticmethod
    def _make_shop_product_key(product_id: int, shop_id: int) -> str:
        return f"product:{product_id}:{shop_id}"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if form.changed_data:
            redis_instance.delete(
                self._make_shop_product_key(form.data["product"], form.data["shop"])
            )
