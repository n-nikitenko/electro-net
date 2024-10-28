from datetime import timedelta
from random import randint

from django.core.management.base import BaseCommand
from django.utils import timezone
from django_seed import Seed

from network.models import NetworkNode, Product


class Command(BaseCommand):
    help = "Генерирует данные о продуктах для узлов сети"

    def add_arguments(self, parser):
        parser.add_argument(
            "--products-per-node",
            type=int,
            default=5,
            help="Среднее количество продуктов на узел сети",
        )

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        products_per_node = options["products_per_node"]

        nodes = NetworkNode.objects.all()

        # Проверка на наличие узлов
        if not nodes.exists():
            self.stdout.write(
                self.style.ERROR(
                    "Нет узлов сети для привязки продуктов. "
                    "Сначала создайте узлы с помощью команды:\n"
                    "  python manage.py generate_network_nodes --nodes-per-level=10"
                )
            )
            return

        for node in nodes:
            # Генерируем случайное количество продуктов для каждого узла в пределах +- 50% от среднего
            num_products = randint(
                int(products_per_node * 0.5), int(products_per_node * 1.5)
            )

            for _ in range(num_products):
                seeder.add_entity(
                    Product,
                    1,
                    {
                        "name": lambda x: f"{seeder.faker.company()} {seeder.faker.word().capitalize()}",
                        "model": lambda x: f"Model-{seeder.faker.random_number(digits=4)}",
                        "release_date": lambda x: timezone.now().date() - timedelta(days=randint(0, 365 * 5)),
                        "network_node": node,
                    },
                )

        # Выполняем генерацию данных продуктов
        inserted_pks = seeder.execute()

        # Выводим количество сгенерированных продуктов
        total_products = sum(len(pks) for pks in inserted_pks.values())
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создано {total_products} продуктов для узлов сети."
            )
        )
