import datetime

import factory
import factory.fuzzy
import pytz

from apps.my_auth.factories import CustomUserFactory

from .models import Friend


class FriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friend

    team_captain = factory.SubFactory(CustomUserFactory)
    teammate = factory.SubFactory(CustomUserFactory)
    status = Friend.STATUS_PENDING
    confirmed = False

    timeRequested = factory.fuzzy.FuzzyDateTime(datetime.datetime(2021, 3, 12,
                                                tzinfo=pytz.utc))
    timeRespondedTo = factory.LazyAttribute(lambda o: o.timeRequested +
                                            datetime.timedelta(minutes=25))
