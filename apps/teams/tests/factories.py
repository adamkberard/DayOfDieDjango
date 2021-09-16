import factory
import factory.fuzzy

from apps.my_auth.tests.factories import CustomUserFactory

from ..models import Team


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    team_captain = factory.SubFactory(CustomUserFactory)
    teammate = factory.SubFactory(CustomUserFactory)
    status = Team.STATUS_PENDING
