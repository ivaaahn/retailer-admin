from django.db import models

# Create your models here.
from django.db.models import TextChoices

from products.models import ProductModel
from shops.models import ShopModel
from user_addresses.models import UserAddressModel
from users.models import UserModel


class OrderProductsModel(models.Model):
    class Meta:
        managed = False
        db_table = "order_products"
        verbose_name = "Продукт заказа"
        verbose_name_plural = "Продукты заказа"

    id = models.BigAutoField(verbose_name="Идентификатор", primary_key=True)
    order = models.ForeignKey(
        "OrderModel",
        models.CASCADE,
        verbose_name="Заказ",
        blank=False,
        null=False,
    )
    product = models.ForeignKey(
        ProductModel,
        models.CASCADE,
        verbose_name="Продукт",
        blank=False,
        null=False,
    )
    price = models.FloatField(
        verbose_name="Стоимость единицы продукта",
        null=False,
        blank=False,
    )
    qty = models.IntegerField(
        verbose_name="Кол-во единиц продукта",
        null=False,
        blank=False,
    )

    def __str__(self) -> str:
        return str(self.product)


class OrderModel(models.Model):
    class Meta:
        managed = False
        db_table = "orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    class OrderReceiveKind(TextChoices):
        takeaway = "takeaway", "Самовывоз"
        delivery = "delivery", "Доставка"

    class OrderStatus(TextChoices):
        collecting = "collecting", "Собирается"
        ready = "ready", "Собран"
        delivering = "delivering", "В пути"
        delivered = "delivered", "Доставлен"
        cancelled = "cancelled", "Отменен"
        finished = "finished", "Завершен"
        error = "error", "Ошибка"

    id = models.BigAutoField(verbose_name="Идентификатор", primary_key=True)
    user = models.ForeignKey(
        UserModel,
        models.CASCADE,
        verbose_name="Клиент",
        blank=False,
        null=False,
    )
    shop = models.ForeignKey(
        ShopModel,
        models.CASCADE,
        verbose_name="Магазин",
        blank=False,
        null=False,
    )
    address = models.ForeignKey(
        UserAddressModel,
        models.CASCADE,
        verbose_name="Адрес доставки",
        blank=True,
        null=True,
    )
    total_price = models.FloatField(
        verbose_name="Стоимость заказа",
        null=False,
        blank=False,
    )
    receive_kind = models.CharField(
        verbose_name="Вид доставки",
        max_length=10,
        choices=OrderReceiveKind.choices,
        default=OrderReceiveKind.takeaway,
        null=False,
        blank=False,
    )
    status = models.CharField(
        verbose_name="Статус заказа",
        max_length=16,
        choices=OrderStatus.choices,
        default=OrderStatus.collecting,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата и время создания заказа",
        null=False,
        auto_now=True,
    )
    products = models.ManyToManyField(
        ProductModel,
        verbose_name="Продукты заказа",
        blank=False,
        through=OrderProductsModel,
    )

    def __str__(self) -> str:
        return f"№{self.pk}"
