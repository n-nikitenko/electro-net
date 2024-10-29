from django_filters import rest_framework as filters

from network.models import NetworkNode, Product


class NetworkNodeCountryFilter(filters.FilterSet):
    """фильтр узлов сети по стране"""

    country = filters.CharFilter(field_name='country', label='Страна')

    class Meta:
        model = NetworkNode
        fields = ['country']


class NetworkProductCountryFilter(filters.FilterSet):
    """фильтр продуктов по стране"""

    country = filters.CharFilter(field_name='network_node__country', label='Страна')

    class Meta(NetworkNodeCountryFilter.Meta):
        model = Product
        fields = ['country']
