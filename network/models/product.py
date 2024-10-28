from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название продукта")

    model = models.CharField(max_length=100, verbose_name="Модель продукта")

    release_date = models.DateField(verbose_name="Дата выхода на рынок")

    # Узел сети, который продаёт этот продукт
    network_node = models.ForeignKey(
        "NetworkNode",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Продающий узел сети",
    )

    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
