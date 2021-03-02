import random

import factory

from apps.my_auth.models import CustomUser

from ..models import Litter


# class CustomUserFactory(factory.django.DjangoModelFactory):
class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: 'User%08d' % n)


class LitterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Litter

    amount = 50


def generateUsername():
    myRange = 10000000
    username = "User{}".format(random.randint(myRange, (myRange * 10) - 1))
    while CustomUser.objects.filter(username=username).count() > 0:
        username = "User{}".format(random.randint(myRange, (myRange * 10) - 1))
    return username
