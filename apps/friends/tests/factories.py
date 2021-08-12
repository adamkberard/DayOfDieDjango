import factory
import factory.fuzzy

from apps.my_auth.tests.factories import CustomUserFactory

from ..models import Friend


class FriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friend

    team_captain = factory.SubFactory(CustomUserFactory)
    teammate = factory.SubFactory(CustomUserFactory)
    status = Friend.STATUS_PENDING
