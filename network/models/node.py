from django.db import models


class NetworkNode(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")

    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=255, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")

    supplier = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="customers",
        verbose_name="Поставщик",
    )

    debt_to_supplier = models.PositiveIntegerField(
        default=0, verbose_name="Задолженность перед поставщиком"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return f"{self.name} ({self.country}), {self.city})"

    def node_type(self):
        if self.supplier is None:
            return "Завод"
        elif self.supplier and self.supplier.supplier is None:
            return "Розничная сеть"
        else:
            return "ИП"

    node_type.short_description = "Тип узла"  # Описание для админки

    class Meta:
        verbose_name = "Узел сети"
        verbose_name_plural = "Узлы сети"
