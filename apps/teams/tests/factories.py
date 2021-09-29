import factory
import factory.fuzzy

from apps.players.tests.factories import PlayerFactory

from ..models import Team


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    team_captain = factory.SubFactory(PlayerFactory)
    teammate = factory.SubFactory(PlayerFactory)
    status = Team.STATUS_PENDING
