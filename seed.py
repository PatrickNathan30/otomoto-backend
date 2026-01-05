import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'otomoto.settings')
django.setup()

from inventory.models import SparePart

fake = Faker()

def create_spare_parts(n=50):
    for _ in range(n):
        SparePart.objects.create(
            name=fake.word().capitalize() + " " + fake.word().capitalize(),
            description=fake.sentence(nb_words=8),
            part_number=fake.unique.bothify(text='???-####'),
            stock=random.randint(1, 1000),
            price=round(random.uniform(10.0, 5000.0), 2),
            location=fake.city()
        )

    print(f"{n} fake spare parts generated!")

if __name__ == '__main__':
    create_spare_parts()
