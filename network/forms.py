from django import forms
from django.db.models import Q

from network.models import NetworkNode


class NetworkNodeAdminForm(forms.ModelForm):
    class Meta:
        model = NetworkNode
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Фильтрация поставщиков: исключаем узлы, которые являются ИП
        self.fields["supplier"].queryset = NetworkNode.objects.filter(
            Q(supplier__isnull=True) | (Q(supplier__isnull=False) & Q(supplier__supplier__isnull=True))
        )
        # Исключаем редактируемый узел
        if self.instance:
            self.fields["supplier"].queryset = self.fields["supplier"].queryset.exclude(
                pk=self.instance.pk
            )
