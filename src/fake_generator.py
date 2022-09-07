from faker import Faker
from datetime import datetime
import random
import uuid
import json

fake = Faker(['pt_BR'])
Faker.seed(0)
companies = [fake.company() for _ in range(50)]


def fake_person_list(count: int):
    bs = [fake.bs() for _ in range(50)]
    company = [fake.company() for _ in range(50)]
    return [{"id": str(uuid.uuid4()),
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
                 "company": random.choice(company),
                 "start": fake.date_between(start_date="-10y", end_date="-1d").isoformat(),
                 "salary": fake.pyfloat(positive=True, min_value=12000, max_value=150000),
             },
             "birthday": fake.date_time_between(start_date="-30y", end_date="-20y").isoformat(),
             "updated_at": datetime.now().isoformat(),
             "status_message": fake.catch_phrase(),
             "status_code": fake.pyint(),
             } for _ in range(count)]


if __name__ == "__main__":
    for p in fake_person_list(10):
        print(json.dumps(p, indent=4, ensure_ascii=False))

