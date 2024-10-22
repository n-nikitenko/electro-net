from rest_framework import serializers

from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    network_node_name = serializers.CharField(source='network_node.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'model',
            'release_date',
            'network_node',
            'network_node_name'
        ]
        read_only_fields = ['id']
