from rest_framework import serializers

from network.models import NetworkNode
from network.serializers.product import ProductSerializer


class NetworkNodeSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            'id',
            'name',
            'email',
            'country',
            'city',
            'street',
            'house_number',
            'supplier',
            'supplier_name',
            'debt_to_supplier',
            'created_at',
            'products'
        ]
        read_only_fields = ['id', 'created_at', 'supplier_name', 'products']

    def validate_supplier(self, supplier):
        """
        Проверка, что поставщик (supplier) находится на более высоком уровне иерархии.
        """

        if supplier is None:
            # Если у звена сети нет поставщика, значит это завод (уровень 0)
            return supplier

        # определение уровеня поставщика
        supplier_level = self.get_network_level(supplier)

        # лпределение уровня текущего звена сети
        current_level = supplier_level + 1

        # Проверяем уровень текущего звена сети
        if current_level > 2:
            raise serializers.ValidationError("Узел сети не может находиться на уровне выше 2.")

        return supplier

    def get_network_level(self, node):
        """
        Рекурсивно вычисляем уровень узла сети на основе его поставщика.
        """
        if node.supplier is None:
            # Если у узла нет поставщика, значит это завод (уровень 0)
            return 0
        else:
            # Рекурсивно вычисляем уровень поставщика
            return self.get_network_level(node.supplier) + 1
