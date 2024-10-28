from django.core.management.base import BaseCommand
from django_seed import Seed

from network.models import NetworkNode


class Command(BaseCommand):
    help = "Заполняет базу данных случайными записями об узлах сети с учётом уровней"

    def add_arguments(self, parser):
        parser.add_argument(
            "--factories", type=int, help="Количество заводов для создания", default=5
        )
        parser.add_argument(
            "--retails",
            type=int,
            help="Количество розничных сетей для создания",
            default=10,
        )
        parser.add_argument(
            "--individuals", type=int, help="Количество ИП для создания", default=15
        )

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        # Генерация заводов (уровень 0)
        seeder.add_entity(
            NetworkNode,
            kwargs["factories"],
            {
                "name": lambda x: seeder.faker.company(),
                "email": lambda x: seeder.faker.email(),
                "country": lambda x: seeder.faker.country(),
                "city": lambda x: seeder.faker.city(),
                "street": lambda x: seeder.faker.street_name(),
                "house_number": lambda x: seeder.faker.building_number(),
                "debt_to_supplier": lambda x: seeder.faker.random_int(
                    min=0, max=10000000
                ),  # Задолженность в копейках
                "supplier": None,  # Заводы не имеют поставщиков
            },
        )

        # Выполнение генерации заводов
        seeder.execute()

        # Генерация розничных сетей (уровень 1, поставщик - завод)
        seeder.add_entity(
            NetworkNode,
            kwargs["retails"],
            {
                "name": lambda x: seeder.faker.company(),
                "email": lambda x: seeder.faker.email(),
                "country": lambda x: seeder.faker.country(),
                "city": lambda x: seeder.faker.city(),
                "street": lambda x: seeder.faker.street_name(),
                "house_number": lambda x: seeder.faker.building_number(),
                "debt_to_supplier": lambda x: seeder.faker.random_int(
                    min=0, max=5000000
                ),
                "supplier": lambda x: NetworkNode.objects.filter(supplier=None)
                .order_by("?")
                .first(),
                # Заводы в качестве поставщиков
            },
        )

        # Выполнение генерации розничных сетей
        seeder.execute()

        # Генерация индивидуальных предпринимателей (уровень 2 и выше)
        seeder.add_entity(
            NetworkNode,
            kwargs["individuals"],
            {
                "name": lambda x: seeder.faker.company(),
                "email": lambda x: seeder.faker.email(),
                "country": lambda x: seeder.faker.country(),
                "city": lambda x: seeder.faker.city(),
                "street": lambda x: seeder.faker.street_name(),
                "house_number": lambda x: seeder.faker.building_number(),
                "debt_to_supplier": lambda x: seeder.faker.random_int(
                    min=0, max=1000000
                ),
                "supplier": lambda x: NetworkNode.objects.exclude(supplier=None)
                .order_by("?")
                .first(),
                # Розничная сеть или другой ИП
            },
        )

        # Выполнение генерации ИП
        seeder.execute()

        self.stdout.write(self.style.SUCCESS("Узлы сети успешно добавлены в иерархию"))
