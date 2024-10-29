from rest_framework import serializers

from network.models import NetworkNode
from network.serializers.product import ProductSerializer
from network.services import get_network_level


class NetworkNodeSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)

    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "supplier_name",
            "debt_to_supplier",
            "created_at",
            "products",
        ]
        read_only_fields = ["id", "created_at", "supplier_name", "debt_to_supplier"]

    def validate_supplier(self, supplier):
        # Проверка, чтобы узел не мог быть своим собственным поставщиком
        if self.instance.supplier and supplier and supplier.id == self.instance.id:
            raise serializers.ValidationError({"supplier": "Узел не может быть своим собственным поставщиком."})

        # Проверка, что поставщик (supplier) находится на более высоком уровне иерархии.
        if supplier is None:
            # Если у звена сети нет поставщика, значит это завод (уровень 0)
            return supplier

        # определение уровеня поставщика
        supplier_level = get_network_level(supplier)

        # лпределение уровня текущего звена сети
        current_level = supplier_level + 1

        # Проверяем уровень текущего звена сети
        if current_level > 2:
            raise serializers.ValidationError(
                {"supplier": "Узел сети не может находиться на уровне выше 2."}
            )

        return supplier


class NetworkNodeUpdateSerializer(NetworkNodeSerializer):
    class Meta(NetworkNodeSerializer.Meta):
        extra_kwargs = {
            'email': {'required': False},
            'country': {'required': False},
            'city': {'required': False},
            'street': {'required': False},
            'house_number': {'required': False},
            'supplier': {'required': False},
        }
