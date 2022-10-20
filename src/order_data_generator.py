from faker import Faker
from datetime import datetime
import random
import uuid
import json

from mimesis import Generic, Person, Food, Finance, Address
from mimesis.locales import Locale
from mimesis.builtins import BrazilSpecProvider

fake = Faker(["pt_BR"])
Faker.seed(0)
companies = [fake.company() for _ in range(50)]
bs = [fake.bs() for _ in range(50)]

generic = Generic(locale=Locale.PT_BR, seed=0xFF)
generic.add_provider(BrazilSpecProvider)
food = Food(locale=Locale.PT_BR)
person = Person(locale=Locale.PT_BR)
finances = Finance(locale=Locale.PT_BR)
address = Address(locale=Locale.PT_BR)
restaurants = [generic.brazil_provider.cnpj() for _ in range(50)]


def fake_person_generator():
    while True:
        yield {
            "id": str(uuid.uuid4()),
            "name": fake.unique.name(),
            "document": fake.unique.cpf(),
            "address": {
                "street": fake.street_name(),
                "number": fake.building_number(),
                "city": fake.city(),
                "state": fake.state_abbr(),
                "zipcode": fake.postcode(),
                "country": fake.country(),
            },
            "contact": {
                "phone": fake.phone_number(),
                "email": fake.email(),
                "cellphone": fake.phone_number(),
            },
            "work": {
                "job": fake.job(),
                "position": random.choice(bs),
                "company": random.choice(companies),
                "start": fake.date_between(
                    start_date="-10y", end_date="-1d"
                ).isoformat(),
                "salary": fake.pyfloat(
                    positive=True, min_value=12000, max_value=150000
                ),
            },
            "academic_degree": person.academic_degree(),
            "university": person.university(),
            "title": person.title(),
            "occupation": person.occupation(),
            "birthday": fake.date_time_between(
                start_date="-30y", end_date="-20y"
            ).isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status_message": fake.catch_phrase(),
            "status_code": fake.pyint(),
        }


def fake_order_generator():
    payment_methods = ["credit_card", "debit_card", "money", "pix"]
    while True:
        total_value, itens = fake_order_itens(random.randint(1, 5))
        yield {
            "id": str(uuid.uuid4()),
            "restaurant": random.choice(restaurants),
            "customer": generic.brazil_provider.cpf(),
            "state": fake.state_abbr(),
            "total_value": total_value,
            "items": itens,
            "payment_method": random.choice(payment_methods),
            "updated_at": datetime.now().isoformat(),
            "status_code": fake.pyint(),
            "lucky_cookie": fake.catch_phrase(),
        }


def fake_order_itens(count: int = 2):
    itens = []
    total_value = 0
    for i in range(count):
        item_value = fake.pyfloat(
            positive=True, min_value=10, max_value=100, right_digits=2
        )
        item_quantity = fake.pyint(min_value=1, max_value=3)
        total_item = item_value * item_quantity
        total_value += total_item
        itens.append(
            {
                "item": i + 1,
                "dish": food.dish(),
                "spices": food.spices(),
                "vegetable": food.vegetable(),
                "fruit": food.fruit(),
                "drink": food.drink(),
                "price": f"{finances.currency_symbol()}{item_value:.2f}",
                "quantity": item_quantity,
                "total": f"{finances.currency_symbol()}{total_item:.2f}",
            }
        )

    return float(f"{total_value:.2f}"), itens


if __name__ == "__main__":
    for _ in range(10):
        print(json.dumps(next(fake_person_generator()), indent=4, ensure_ascii=False))
        print(json.dumps(next(fake_order_generator()), indent=4, ensure_ascii=False))
