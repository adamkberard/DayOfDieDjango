import random

import factory
from faker import Faker
from faker.factory import Factory

from .models import CustomUser

Faker = Factory.create

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Faker('email')
    username = factory.Sequence(lambda n: "User%05d" % n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
