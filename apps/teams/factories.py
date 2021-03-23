import datetime

import factory
import factory.fuzzy
import pytz

from apps.my_auth.factories import CustomUserFactory

from .models import Team


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    teamCaptain = factory.SubFactory(CustomUserFactory)
    teammate = factory.SubFactory(CustomUserFactory)
    status = Team.PENDING
    league = Team.BRONZE

    timeRequested = factory.fuzzy.FuzzyDateTime(datetime.datetime(2021, 3, 12,
                                                tzinfo=pytz.utc))
    timeRespondedTo = factory.LazyAttribute(lambda o: o.timeRequested +
                                            datetime.timedelta(minutes=25))
